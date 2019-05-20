from config import DBMS
from service.article_service import ArticleService
from service.read_service import ReadService
from service.user_service import UserService
from test.test_base import TestBase


class TestReadService(TestBase):

    def setup_method(self) -> None:
        self.readService = ReadService()

    def test_count(self):
        for dbms in DBMS.all:
            cnt = self.readService.count(db_alias=dbms)
            print("count {}: {}".format(dbms, cnt))

    def test_save_read(self):
        article = ArticleService().get_articles_by_title('title4')[0]
        user = UserService().get_user_by_name('user4')
        read = self.readService.save_read(article.aid, user.uid, 1, 34, 2, 0, 'sdf', 1, 1)

        assert read is not None
        print(read)
        return read

    def test_reads_list(self):
        reads = self.readService.get_reads()
        assert reads is not None
        self.readService.pretty_reads(reads)

        reads = self.readService.get_reads(db_alias=DBMS.DBMS1)
        assert reads is not None
        self.readService.pretty_reads(reads)

    def test_del_read_by_id(self):
        read = self.test_save_read()
        num = self.readService.del_read_by_id(read.id)
        print(num)
        # assert num == 1

    def test_del_reads_by_uid(self):
        user = UserService().get_user_by_name('user4')
        num = self.readService.del_reads_by_uid(user.uid)
        print(num)
        # assert num > 0

    def test_get_history(self):
        user = UserService().get_user_by_name('user4')
        reads = self.readService.get_history(str(user.uid))
        self.readService.pretty_reads(reads)

    def test__get_popular(self):
        from utils.func import merge_dict_and_sort
        start = 1506332297000
        end = 1506332347001
        # [{'_id': 237, 'count': 1}
        read1 = self.readService._ReadService__get_popular_by_freq(start, end, db_alias=DBMS.DBMS2)
        read2 = self.readService._ReadService__get_popular_by_freq(start, end, db_alias=DBMS.DBMS1)
        print(merge_dict_and_sort(read1, read2))

        read1 = self.readService._ReadService__get_popular_by_aggregate(start, end, db_alias=DBMS.DBMS2)
        read2 = self.readService._ReadService__get_popular_by_aggregate(start, end, db_alias=DBMS.DBMS1)
        print(merge_dict_and_sort(read1, read2))
        pass

    def test_get_popular(self):
        from utils.func import timestamp_to_datetime
        _date = timestamp_to_datetime(1506338537000)

        reads = self.readService.compute_popular(_date.date(), before_days=7)
        print(reads)

    def test_get_daily_popular(self):
        # TODO 测试数据量大的时候导入热门数据
        from utils.func import timestamp_to_datetime
        _date = timestamp_to_datetime(1506340567000)

        reads = self.readService.get_daily_popular(_date.date())
        print(reads)

    def test_get_weekly_popular(self):
        from utils.func import timestamp_to_datetime
        _date = timestamp_to_datetime(1506340567000)

        reads = self.readService.get_weekly_popular(_date.date())
        print(reads)

    def test_get_month_popular(self):
        from utils.func import timestamp_to_datetime
        _date = timestamp_to_datetime(1506342197000)

        reads = self.readService.get_monthly_popular(_date.date())
        print(reads)
