from datetime import datetime, timedelta
import unittest

from celly.cogs.schedule import ScheduleUpdateCog


class TestScheduleUpdateCog(unittest.TestCase):
    def setUp(self):
        self.cog = ScheduleUpdateCog()

    def test_is_day_complete_no_games(self):
        day = {
            "date": "2018-10-04",
            "totalGames": 0,
        }
        assert self.cog._is_day_complete(day)

    def test_is_day_complete_1_game(self):
        day = {
            "date": "2018-10-04",
            "totalGames": 1,
            "games": [
                {
                    "status": {
                        "abstractGameState": "Preview"
                    }
                }
            ]
        }
        assert not self.cog._is_day_complete(day)

    def test_is_day_complete_1_game(self):
        day = {
            "date": "2018-10-04",
            "totalGames": 1,
            "games": [
                {
                    "status": {
                        "abstractGameState": "Final"
                    }
                }
            ]
        }
        assert self.cog._is_day_complete(day)

    def test_is_day_complete_multi_game(self):
        day = {
            "date": "2018-10-04",
            "totalGames": 1,
            "games": [
                {
                    "status": {
                        "abstractGameState": "Final"
                    }
                },
                {
                    "status": {
                        "abstractGameState": "Preview"
                    }
                }
            ]
        }
        assert not self.cog._is_day_complete(day)

    def test_last_update(self):
        sched = [{
            "date": "2018-10-04",
            "totalGames": 1,
            "games": [
                {
                    "status": {
                        "abstractGameState": "Final"
                    }
                },
                {
                    "status": {
                        "abstractGameState": "Final"
                    }
                }
            ]
        },
        {
            "date": "2018-10-05",
            "totalGames": 1,
            "games": [
                {
                    "status": {
                        "abstractGameState": "Final"
                    }
                },
                {
                    "status": {
                        "abstractGameState": "Preview"
                    }
                }
            ]
        }]
        assert self.cog._last_update(sched) == "2018-10-05"

    def test_merge_new_schedule(self):
        old_sched = [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
                "marker": 1,
            },
        ]
        new_data = {
            "dates": [
                {
                    "date": "2018-10-05",
                    "marker": 2,
                },
                {
                    "date": "2018-10-06",
                },
                {
                    "date": "2018-10-07",
                }
            ]
        }

        merged = self.cog._merge_new_schedule(old_sched, new_data)
        assert merged == [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
                "marker": 2,
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
            },
        ]

    def test_sanitize_schedule_missing_start(self):
        sched = [
            # {
            #     "date": "2018-10-04",
            # },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
            },
        ]
        start = datetime.strptime("2018-10-04", "%Y-%m-%d")
        end = datetime.strptime("2018-10-07", "%Y-%m-%d")
        san_sched = self.cog._sanitize_schedule(sched, start, end)
        assert san_sched == [
            {
                "date": "2018-10-04",
                "totalGames": 0,
                "games": [],
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
            },
        ]

    def test_sanitize_schedule_missing_mid(self):
        sched = [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            # {
            #     "date": "2018-10-06",
            # },
            {
                "date": "2018-10-07",
            },
            {
                "date": "2018-10-08",
            },
        ]
        start = datetime.strptime("2018-10-04", "%Y-%m-%d")
        end = datetime.strptime("2018-10-08", "%Y-%m-%d")
        san_sched = self.cog._sanitize_schedule(sched, start, end)
        assert san_sched == [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
                "totalGames": 0,
                "games": [],
            },
            {
                "date": "2018-10-07",
            },
            {
                "date": "2018-10-08",
            },
        ]

    def test_sanitize_schedule_missing_end(self):
        sched = [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            # {
            #     "date": "2018-10-07",
            # },
        ]
        start = datetime.strptime("2018-10-04", "%Y-%m-%d")
        end = datetime.strptime("2018-10-07", "%Y-%m-%d")
        san_sched = self.cog._sanitize_schedule(sched, start, end)
        assert san_sched == [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
                "totalGames": 0,
                "games": [],
            },
        ]

    def test_sanitize_schedule_missing_none(self):
        sched = [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
            },
        ]
        start = datetime.strptime("2018-10-04", "%Y-%m-%d")
        end = datetime.strptime("2018-10-07", "%Y-%m-%d")
        san_sched = self.cog._sanitize_schedule(sched, start, end)
        assert san_sched == [
            {
                "date": "2018-10-04",
            },
            {
                "date": "2018-10-05",
            },
            {
                "date": "2018-10-06",
            },
            {
                "date": "2018-10-07",
            },
        ]
