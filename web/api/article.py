import datetime
import logging

from flask import request, Blueprint

from config import DBMS
from service.article_service import ArticleService
from service.redis_service import RedisService
from utils.func import get_best_dbms_by_category, check_alias, DbmsAliasError
from web.result import Result

articles = Blueprint('articles', __name__)

logger = logging.getLogger('api_articles')

# Redis KEY 设置
ARTICLES = 'ARTICLES'
ARTICLES_LIST = f"{ARTICLES}:LIST"
ARTICLES_ITEM = f"{ARTICLES}:ITEM"


@articles.route('', methods=['GET'])
def get_articles():
    # 获取请求参数
    page_num = int(request.args.get('page', 1))  # 页码
    page_size = int(request.args.get('size', 20))  # 每页数量
    dbms = request.args.get('dbms')  # 请求数据库
    sort_by = request.args.get('sort_by')
    if sort_by is not None and sort_by not in ArticleService.field_names:
        if sort_by[1:] not in ArticleService.field_names:
            sort_by = None

    try:  # 检查数据库地址正确性
        check_alias(db_alias=dbms)
    except DbmsAliasError:
        return Result.gen_failed('404', 'dbms error')

    # 获取查询参数
    title = request.args.get('title')
    authors = request.args.get('authors')
    category = request.args.get('category')
    articleTags = request.args.get('articleTags')
    language = request.args.get('language')
    detail = request.args.get('detail', '1')
    # print(request.data)
    # print(exclude)

    cons = {
        'title__contains': title,
        'authors': authors,
        'category': category,
        'articleTags': articleTags,
        'language': language
    }
    # 去除为空的查询参数
    kwargs = {}
    for key, value in cons.items():
        if value is not None and value != '':
            kwargs[key] = value

    if detail != '1':
        kwargs['exclude'] = ['text', 'image', 'video']

    # 尝试从dbms对应的Redis中获取该数据
    _REDIS_KEY_ = f"{ARTICLES_LIST}:{dbms}:{page_num}:{page_size}:{sort_by}:{kwargs}"
    data = RedisService().get_dict(dbms, _REDIS_KEY_)
    # 判断数据是否存在
    if data is None or data == {}:
        # 不存在
        arts = ArticleService().get_articles(page_num=page_num, page_size=page_size, db_alias=dbms, sort_by=sort_by,
                                             **kwargs)
        arts = list(art.to_dict() for art in arts)
        total = ArticleService().count(db_alias=dbms, **kwargs)
        data = {
            'total': total,
            'list': arts
        }

        # 将该数据存入Redis中
        RedisService().set_dict(dbms, _REDIS_KEY_, data)
    return Result.gen_success(data)
    pass


@articles.route('', methods=['POST'])
def new_articles():
    data = request.json
    for key in list(data.keys())[::-1]:
        if key not in ArticleService.field_names:
            data.pop(key)

    logger.info(f'添加文章： {data}')
    # 先删除对应的缓存，然后在添加文章
    for dbms in DBMS().get_dbms_by_category(data['category']):
        RedisService().delete_key_by_pattern(dbms, f'{ARTICLES_LIST}:*')

    aid = ArticleService().add_an_article(**data)

    return Result.gen_success(data={'aid': aid})
    pass


@articles.route('/<int:aid>', methods=['GET'])
def get_article(aid):
    if aid is None:
        return Result.gen_failed('404', 'aid not found')
    # 获取查询参数
    category = request.args.get('category', None)

    # article = {}

    # 尝试从Redis中获取该数据
    _REDIS_KEY_ = f"{ARTICLES_ITEM}:{aid}"
    if category is not None:

        if category not in DBMS().category['values']:
            return Result.gen_failed('404', '类别不存在')

        # 从category对应的dbms的redis中取数据
        dbms = get_best_dbms_by_category(category)
        article = RedisService().get_dict(dbms, _REDIS_KEY_)
        if article == {}:
            # 缓存中无数据，则去数据库中查询
            article = ArticleService().get_one_by_aid(aid=aid,
                                                      db_alias=get_best_dbms_by_category(category))
            if article is not None:
                # article存在，存入redis中
                article = article.to_dict()
                RedisService().set_dict(dbms, _REDIS_KEY_, article)
    else:
        # 尝试从所有redis中取该数据
        article = RedisService().get_dict_from_all(_REDIS_KEY_)
        if article == {}:
            # 缓存中没有，去数据库中查询
            article = ArticleService().get_one_by_aid(aid=aid)
            if article is not None:
                article = article.to_dict()
                try:
                    for dbms in DBMS().get_dbms_by_category(article['category']):
                        RedisService().set_dict(dbms, _REDIS_KEY_, article)
                except Exception:
                    #  避免出现类别不存在的情况
                    logger.info(f"aid: {aid} 存入缓存失败， data: {article}")

    if article is None or article == {}:
        return Result.gen_failed(404, '文章不存在')
    return Result.gen_success(article)


@articles.route('/<int:aid>', methods=['DELETE'])
def delete_article(aid):
    if aid is None:
        return Result.gen_failed('404', 'aid not found')

    _REDIS_KEY_ = f"{ARTICLES_ITEM}:{aid}"

    category = request.args.get('category')
    if category is None:
        return Result.gen_failed('5000', '请带上category参数')

    # 先从缓存中删除该键值以及所有list对应的键值
    for dbms in DBMS().get_dbms_by_category(category):
        RedisService().delete_key(dbms, _REDIS_KEY_)
        RedisService().delete_key_by_pattern(dbms, f"{ARTICLES_LIST}:*")

    ArticleService().del_by_aid(aid)

    return Result.gen_success('删除成功')


@articles.route('/<int:aid>', methods=['POST'])
def update_article(aid):
    data = request.json
    category = data.pop('category', None)
    if category is None:
        return Result.gen_failed(code=5000, msg='缺少category字段')

    for key in list(data.keys())[::-1]:
        if key not in ArticleService.field_names or key in ArticleService.update_forbid:
            data.pop(key)

    data['update_time'] = datetime.datetime.now()

    # print(data)
    _REDIS_KEY_ = f"{ARTICLES_ITEM}:{aid}"

    for dbms in DBMS().get_dbms_by_category(category):
        RedisService().delete_key(dbms, _REDIS_KEY_)
        RedisService().delete_key_by_pattern(dbms, f"{ARTICLES_LIST}:*")

        ArticleService().update_by_aid(aid=aid, db_alias=dbms, **data)

    return Result.gen_success(data={'aid': aid, 'category': category})

# class ArticleList(MethodView):
#     def get(self):
#         # 获取请求参数
#         page_num = int(request.args.get('page', 1))  # 页码
#         page_size = int(request.args.get('size', 20))  # 每页数量
#         dbms = request.args.get('dbms')  # 请求数据库
#         sort_by = request.args.get('sort_by')
#         if sort_by is not None and sort_by not in ArticleService.field_names:
#             if sort_by[1:] not in ArticleService.field_names:
#                 sort_by = None
#
#         try:  # 检查数据库地址正确性
#             check_alias(db_alias=dbms)
#         except DbmsAliasError:
#             return Result.gen_failed('404', 'dbms error')
#
#         # 获取查询参数
#         title = request.args.get('title')
#         authors = request.args.get('authors')
#         category = request.args.get('category')
#         articleTags = request.args.get('articleTags')
#         language = request.args.get('language')
#         detail = request.args.get('detail', '1')
#         # print(request.data)
#         # print(exclude)
#
#         cons = {
#             'title__contains': title,
#             'authors': authors,
#             'category': category,
#             'articleTags': articleTags,
#             'language': language
#         }
#         # 去除为空的查询参数
#         kwargs = {}
#         for key, value in cons.items():
#             if value is not None and value != '':
#                 kwargs[key] = value
#
#         if detail != '1':
#             kwargs['exclude'] = ['text', 'image', 'video']
#
#         # 尝试从dbms对应的Redis中获取该数据
#         _REDIS_KEY_ = f"ARTICLE_LIST:{dbms}:{page_num}:{page_size}:{kwargs}:{sort_by}"
#         data = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
#         # 判断数据是否存在
#         if data is None or data == {}:
#             # 不存在
#             arts = ArticleService().get_articles(page_num=page_num, page_size=page_size, db_alias=dbms, sort_by=sort_by,
#                                                  **kwargs)
#             arts = list(art.to_dict() for art in arts)
#             total = ArticleService().count(db_alias=dbms, **kwargs)
#             data = {
#                 'total': total,
#                 'list': arts
#             }
#             # 将该数据存入Redis中
#             RedisService().get_redis(dbms).set_dict(_REDIS_KEY_, data)
#         return Result.gen_success(data)
#         pass
#
#     def post(self):
#         data = request.json
#
#         for key in list(data.keys())[::-1]:
#             if key not in ArticleService.field_names:
#                 data.pop(key)
#
#         print(data)
#         aid = ArticleService().add_an_article(**data)
#
#         return Result.gen_success(data={'aid': aid})
#         pass


# class ArticleCURD(MethodView):
#     def get(self, aid):
#
#         if aid is None:
#             return Result.gen_failed('404', 'aid not found')
#         # 获取查询参数
#         category = request.args.get('category', None)
#
#         # 尝试从Redis中获取该数据
#         _REDIS_KEY_ = f"ARTICLE:{aid}"
#         if category is not None:
#
#             if category not in DBMS().category['values']:
#                 return Result.gen_failed('404', '类别不存在')
#
#             # 从category对应的dbms的redis中取数据
#             article = RedisService().get_redis(get_best_dbms_by_category(category)).get_dict(_REDIS_KEY_)
#             if article == {}:
#
#                 article = ArticleService().get_one_by_aid(aid=aid,
#                                                           db_alias=get_best_dbms_by_category(category))
#                 if article is not None:
#                     article = article.to_dict()
#                     RedisService().get_redis(get_best_dbms_by_category(category)).set_dict(_REDIS_KEY_, article)
#         else:
#             article = {}
#             # 尝试从所有redis中取该数据
#             for dbms in DBMS().get_all_dbms_by_category():
#                 article = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
#                 if article != {}:
#                     break
#             if article == {}:
#                 article = ArticleService().get_one_by_aid(aid=aid)
#                 if article is not None:
#                     article = article.to_dict()
#                     RedisService().get_redis(get_best_dbms_by_category(article['category'])).set_dict(_REDIS_KEY_,
#                                                                                                       article)
#
#         if article is None:
#             return Result.gen_failed(404, '文章不存在')
#         return Result.gen_success(article)
#
#     def delete(self, aid):
#         if aid is None:
#             return Result.gen_failed('404', 'aid not found')
#
#         category = request.args.get('category')
#         if category is None:
#             return Result.gen_failed('5000', '请带上category参数')
#         # 先从缓存中删除该键值以及所有list对应的键值
#         dbms = DBMS().get_best_dbms_by_category(category)
#         RedisService().get_redis(dbms).delete(f'ARTICLE:{aid}')
#         RedisService().get_redis(dbms).delete_by_pattern(f"ARTICLE_LIST:{dbms}:*")
#
#         ArticleService().del_by_aid(aid)
#
#         return Result.gen_success('删除成功')
#
#     def post(self, aid):
#         data = request.json
#         category = data.pop('category', None)
#         if category is None:
#             return Result.gen_failed(code=5000, msg='缺少category字段')
#
#         for key in list(data.keys())[::-1]:
#             if key not in ArticleService.field_names or key in ArticleService.update_forbid:
#                 data.pop(key)
#
#         data['update_time'] = datetime.datetime.now()
#
#         print(data)
#
#         for dbms in DBMS().get_dbms_by_category(category):
#             ArticleService().update_by_aid(aid=aid, db_alias=dbms, **data)
#
#         return Result.gen_success(data={'aid': aid, 'category': category})
