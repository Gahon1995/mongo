from flask import request
from flask.views import MethodView

from config import DBMS
from service.article_service import ArticleService
from utils.func import get_best_dbms_by_category
from utils.result import Result


class ArticleList(MethodView):
    def get(self):
        page_num = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 20))
        arts = ArticleService().get_articles(page_num=page_num, page_size=page_size, db_alias=DBMS.DBMS1)
        arts = list(art.to_dict() for art in arts)
        total = ArticleService().count(db_alias=DBMS.DBMS1)
        data = {
            'total': total,
            'list': arts
        }
        return Result.gen_success(data)
        pass


class ArticleCURD(MethodView):
    def get(self, aid):
        # aid = request.args.get('aid', None)
        if aid is None:
            return Result.gen_failed('404', 'aid not found')
        category = request.args.get('category', None)
        if category is not None:
            article = ArticleService().get_one_by_aid(aid=aid, db_alias=get_best_dbms_by_category(category))
        else:
            article = ArticleService().get_one_by_aid(aid=aid)
        return Result.gen_success(article)

    def delete(self, aid):
        if aid is None:
            return Result.gen_failed('404', 'aid not found')

        ArticleService().del_by_aid(aid)

        return Result.gen_success('删除成功')
