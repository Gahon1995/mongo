from flask import request
from flask.views import MethodView

from config import DBMS
from service.popular_service import PopularService
from utils.func import get_best_dbms_by_category
from web.api.result import Result


class PopularList(MethodView):
    def get(self):
        page_num = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 20))
        arts = PopularService().get_daily_articles(_date=123)
        arts = list(art.to_dict() for art in arts)
        total = PopularService().count(db_alias=DBMS.DBMS1)
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
