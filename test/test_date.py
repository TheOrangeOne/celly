import unittest
from celly.date import prev_ymd, next_ymd


class TestDateUtils(unittest.TestCase):
    def test_prev_ymd(self):
        assert prev_ymd("2018-10-04") == "2018-10-03"
        assert prev_ymd("2018-10-01") == "2018-09-30"
        assert prev_ymd("2018-01-01") == "2017-12-31"

    def test_next_ymn(self):
        assert next_ymd("2018-10-04") == "2018-10-05"
        assert next_ymd("2018-10-01") == "2018-10-02"
