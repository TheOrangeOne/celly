import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogs.games import GamesCog, CompletedRegSeasonGamesCog
from celly.cogwheel import CogWheel

"""
class TestGamesCog(unittest.TestCase):
    def setUp(self):
        self.wheel = CogWheel()

    def test_schedule_integration(self):
        self.wheel.add(Cog(
            name="sched",
            output=lambda: [
                {
                    "date": "2018-10-04",
                    "totalGames": 1,
                    "games": [
                        {
                            "gameType": "R",
                            "season": "20182019",
                        }
                    ]
                }
            ]
        ))
        self.wheel.add(GamesCog(
            name="gamedata",
            inputs=["sched"],
        ))

        cog = Cog("check", inputs=["gamedata"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with([
            {
                "gameType": "R",
                "season": "20182019",
            }
        ])

    def test_completed_regular_season_games(self):
        self.wheel.add(Cog(
            name="currentseason",
            output=lambda: "20182019"
        ))
        self.wheel.add(Cog(
            name="sched",
            output=lambda: [
                {
                    "date": "2018-10-04",
                    "totalGames": 1,
                    "games": [
                        {
                            "gameType": "R",
                            "gameDate": "2018-10-04",
                            "season": "20182019",
                            "marker": 1,
                            "status": {
                                "abstractGameState": "Final",
                            },
                        }
                    ]
                },
                {
                    "date": "2018-10-05",
                    "totalGames": 2,
                    "games": [
                        {
                            "gameType": "R",
                            "gameDate": "2018-10-05",
                            "season": "20182019",
                            "marker": 2,
                            "status": {
                                "abstractGameState": "Final",
                            },
                        },
                        {
                            "gameType": "R",
                            "gameDate": "2018-10-05",
                            "season": "20182019",
                            "marker": 3,
                            "status": {
                                "abstractGameState": "Final",
                            },
                        },
                        {
                            "gameType": "P",
                            "gameDate": "2018-10-05",
                            "season": "20182019",
                            "marker": 4,
                            "status": {
                                "abstractGameState": "Final",
                            },
                        },
                        {
                            "gameType": "R",
                            "gameDate": "2018-10-05",
                            "season": "20192020",
                            "marker": 5,
                            "status": {
                                "abstractGameState": "Final",
                            },
                        },
                        {
                            "gameType": "R",
                            "gameDate": "2018-10-05",
                            "season": "20182019",
                            "marker": 7,
                            "status": {
                                "abstractGameState": "Preview",
                            },
                        },
                    ]
                }
            ]
        ))
        self.wheel.add(CompletedRegSeasonGamesCog(
            name="completedgames",
            inputs=["currentseason", "sched"]
        ))

        cog = Cog("check", inputs=["completedgames"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
            "2018-10-04": [
                {
                    "gameType": "R",
                    "gameDate": "2018-10-04",
                    "season": "20182019",
                    "marker": 1,
                    "status": {
                        "abstractGameState": "Final",
                    },
                },
            ],
            "2018-10-05": [
                {
                    "gameType": "R",
                    "gameDate": "2018-10-05",
                    "season": "20182019",
                    "marker": 2,
                    "status": {
                        "abstractGameState": "Final",
                    },
                },
                {
                    "gameType": "R",
                    "gameDate": "2018-10-05",
                    "season": "20182019",
                    "marker": 3,
                    "status": {
                        "abstractGameState": "Final",
                    },
                }
            ]
        })
"""
