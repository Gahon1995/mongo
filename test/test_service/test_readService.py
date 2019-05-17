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
            print("count {}: {}".format(getattr(DBMS, dbms), cnt))

    def test_save_read(self):
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
        import datetime
        start = datetime.date(2017, 9, 25)
        end = datetime.date(2017, 9, 26)

        reads = self.readService.get_popular(start, end, db_alias=DBMS.DBMS1)

        print(reads)
        pass

    def test_get_popular(self):
        self.fail()

    def test_get_daily_popular(self):
        self.fail()

    def test_get_weekly_popular(self):
        self.fail()

    def test_get_month_popular(self):
        self.fail()
