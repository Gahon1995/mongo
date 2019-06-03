from flask import request
from flask.views import MethodView

from config import DBMS
from service.article_service import ArticleService
from service.redis_service import RedisService
from utils.func import get_best_dbms_by_category, check_alias, DbmsAliasError
from web.api.result import Result


class ArticleList(MethodView):
    def get(self):
        # 获取请求参数
        page_num = int(request.args.get('page', 1))  # 页码
        page_size = int(request.args.get('size', 20))  # 每页数量
        dbms = request.args.get('dbms')  # 请求数据库
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
        _REDIS_KEY_ = f"ARTICLE_LIST:{dbms}:{page_num}:{page_size}:{kwargs}"
        data = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
        # 判断数据是否存在
        if data is None or data == {}:
            # 不存在
            arts = ArticleService().get_articles(page_num=page_num, page_size=page_size, db_alias=dbms, **kwargs)
            arts = list(art.to_dict() for art in arts)
            total = ArticleService().count(db_alias=dbms, **kwargs)
            data = {
                'total': total,
                'list': arts
            }
            # 将该数据存入Redis中
            RedisService().get_redis(dbms).set_dict(_REDIS_KEY_, data)
        return Result.gen_success(data)
        pass


class ArticleCURD(MethodView):
    def get(self, aid):

        if aid is None:
            return Result.gen_failed('404', 'aid not found')
        # 获取查询参数
        category = request.args.get('category', None)

        # 尝试从Redis中获取该数据
        _REDIS_KEY_ = f"ARTICLE:{aid}"
        if category is not None:
            # 从category对应的dbms的redis中取数据
            article = RedisService().get_redis(get_best_dbms_by_category(category)).get_dict(_REDIS_KEY_)
            if article == {}:
                article = ArticleService().get_one_by_aid(aid=aid,
                                                          db_alias=get_best_dbms_by_category(category)).to_dict()
                RedisService().get_redis(get_best_dbms_by_category(category)).set_dict(_REDIS_KEY_, article)
        else:
            article = {}
            # 尝试从所有redis中取该数据
            for dbms in DBMS().get_all_dbms_by_category():
                article = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
                if article != {}:
                    break
            if article == {}:
                article = ArticleService().get_one_by_aid(aid=aid).to_dict()
                RedisService().get_redis(get_best_dbms_by_category(article.category)).set_dict(_REDIS_KEY_, article)
        return Result.gen_success(article)

    def delete(self, aid):
        if aid is None:
            return Result.gen_failed('404', 'aid not found')

        category = request.args.get('category')
        if category is None:
            return Result.gen_failed('5000', '请带上category参数')
        # 先从缓存中删除该键值以及所有list对应的键值
        dbms = DBMS().get_best_dbms_by_category(category)
        RedisService().get_redis(dbms).delete(f'ARTICLE:{aid}')
        RedisService().get_redis(dbms).delete_by_pattern(f"ARTICLE_LIST:{dbms}:*")

        ArticleService().del_by_aid(aid)

        return Result.gen_success('删除成功')
