from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest import mock

from celly.cog import Cog
from celly.cogs.schedule import ScheduleUpdateCog
from ..cog_utils import TestCase, TestCog


class TestScheduleUpdateCog(TestCase):
    def setUp(self):
        super().setUp()
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
        assert self.cog._last_update(sched, "2018-10-03") == "2018-10-05"

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

    @mock.patch("celly.web.get_json")
    def test_no_cache(self, mock_get_json):
        mock_get_json.return_value = {
            "totalItems": 1,
            "totalGames": 1,
            "dates": [{
                "date": "2018-10-11",
                "totalItems": 1,
                "totalGames": 1,
                "games": [ {
                    "gameType" : "R",
                    "season" : "20182019",
                    "gameDate" : "2018-10-12T00:00:00Z",
                    "status" : {
                        "abstractGameState" : "Final",
                    },
                    "teams" : {
                        "away" : {
                            "leagueRecord" : {
                                "wins" : 2,
                                "losses" : 0,
                                "ot" : 2,
                                "type" : "league"
                            },
                            "score" : 3,
                            "team" : {
                                "id" : 16,
                                "name" : "Chicago Blackhawks",
                            }
                        },
                        "home" : {
                            "leagueRecord" : {
                                "wins" : 1,
                                "losses" : 1,
                                "ot" : 1,
                                "type" : "league"
                            },
                            "score" : 4,
                            "team" : {
                                "id" : 30,
                                "name" : "Minnesota Wild",
                            }
                        }
                    },
                    "linescore" : {
                        "currentPeriod" : 4,
                        "currentPeriodOrdinal" : "OT",
                        "currentPeriodTimeRemaining" : "Final",
                        "teams" : {
                            "home" : {
                                "team" : {
                                    "id" : 30,
                                    "name" : "Minnesota Wild",
                                },
                                "goals" : 4,
                                "shotsOnGoal" : 46,
                            },
                            "away" : {
                                "team" : {
                                    "id" : 16,
                                    "name" : "Chicago Blackhawks",
                                },
                                "goals" : 3,
                                "shotsOnGoal" : 30,
                            }
                        },
                    },
                }],
            }]
        }
        self.wheel.add(Cog(
            name="cached_sched",
            output=lambda: None
        ))
        self.wheel.add(Cog(
            name="season_start",
            output=lambda: "2018-10-10"
        ))
        self.wheel.add(Cog(
            name="today",
            output=lambda: datetime.strptime("2018-10-12", "%Y-%m-%d")
        ))
        self.wheel.add(ScheduleUpdateCog(
            name="sched",
            inputs=dict(
                cached_sched="cached_sched",
                season_start="season_start",
                now="today",
            )
        ))

        testcog = TestCog(
            inputs=dict(sched="sched"),
            should_be_called_with=dict(
                sched=[
                    {
                        'date': '2018-10-10',
                        'totalGames': 0,
                        'games': []
                    },
                    {
                        'date': '2018-10-11',
                        'totalItems': 1,
                        'totalGames': 1,
                        'games': [{
                            'gameType': 'R',
                            'season': '20182019',
                            'gameDate': '2018-10-12T00:00:00Z',
                            'status': {'abstractGameState': 'Final'},
                            'teams': {
                                'away': {
                                    'leagueRecord': {
                                        'wins': 2,
                                        'losses': 0,
                                        'ot': 2,
                                        'type': 'league'
                                    },
                                    'score': 3,
                                    'team': {
                                        'id': 16,
                                        'name': 'Chicago Blackhawks'
                                    }
                                 },
                                'home': {
                                    'leagueRecord': {
                                        'wins': 1,
                                        'losses': 1,
                                        'ot': 1,
                                        'type': 'league'
                                    },
                                    'score': 4,
                                    'team': {
                                        'id': 30,
                                        'name': 'Minnesota Wild'
                                    }
                                }
                            },
                            'linescore': {
                                'currentPeriod': 4,
                                'currentPeriodOrdinal': 'OT',
                                'currentPeriodTimeRemaining': 'Final',
                                 'teams': {
                                     'home': {
                                         'team': {
                                             'id': 30,
                                             'name': 'Minnesota Wild'
                                         },
                                         'goals': 4,
                                         'shotsOnGoal': 46
                                     },
                                     'away': {
                                         'team': {
                                             'id': 16,
                                             'name': 'Chicago Blackhawks',
                                         },
                                         'goals': 3,
                                         'shotsOnGoal': 30
                                     }
                                 }
                            }
                        }]
                    }, {
                        'date': '2018-10-12',
                        'totalGames': 0,
                        'games': []
                    }
                ]
            )
        )
        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()
