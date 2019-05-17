from test.test_base import TestBase

from service.read_service import ReadService
from config import DBMS


class TestReadService(TestBase):

    def setup_method(self) -> None:
        self.readService = ReadService()

    def test_get_id(self):
        rid = self.readService.get_id()
        print("rid: ", str(rid))

    def test_count(self):
        for dbms in DBMS.all:
            cnt = self.readService.count(db_alias=dbms)
            print("count {}: {}".format(dbms, cnt))

    def test_save_read(self):
        read = self.readService.save_read(1, 0, 1, 34, 2, 0, 'sdf', 1, 1)
        if read is None:
            read = self.readService.save_read(1, 1, 1, 34, 2, 0, 'sdf', 1, 1)
        if read is None:
            read = self.readService.save_read(0, 0, 1, 34, 2, 0, 'sdf', 1, 1)
        if read is None:
            read = self.readService.save_read(0, 1, 1, 34, 2, 0, 'sdf', 1, 1)

        assert read is not None
        print(read)

    def test_reads_list(self):
        reads = self.readService.get_reads()
        assert reads is not None
        self.readService.pretty_reads(reads)

        reads = self.readService.get_reads(db_alias=DBMS.DBMS1)
        assert reads is not None
        self.readService.pretty_reads(reads)

    def test_del_read_by_rid(self):
        num = self.readService.del_read_by_rid(85)
        print(num)
        # assert num == 1

    def test_del_reads_by_uid(self):
        num = self.readService.del_reads_by_uid(35)
        print(num)
        # assert num > 0

    def test_get_history(self):
        reads = self.readService.get_history(21)
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

        reads = self.readService.get_month_popular(_date.date())
        print(reads)
