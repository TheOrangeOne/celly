import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogwheel import CogWheel
from celly.cogs.ratings import RatingsCog, NormedRatingsCog


class TestRatingsCog(unittest.TestCase):
    def setUp(self):
        self.wheel = CogWheel()

    def test_ratings_basic(self):
        self.wheel.add(Cog(
            name="games",
            output=lambda: [
                {
                    "gameType": "R",
                    "season": "20182019",
                    "teams": {
                        "home": {
                            "team": {
                                "id": 1,
                            },
                            "score": 3,
                        },
                        "away": {
                            "team": {
                                "id": 2,
                            },
                            "score": 2,
                        },
                    },
                    "linescore": {
                        "currentPeriod": 3
                    },
                },
            ]
        ))
        self.wheel.add(RatingsCog(
            name="ratings",
            inputs=["games"],
        ))

        cog = Cog("check", inputs=["ratings"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
            1: {
                "rating": 1507.5,
                "gp": 1,
            },
            2: {
                "rating": 1492.5,
                "gp": 1,
            }
        })

    def test_normed_ratings_basic(self):
        self.wheel.add(Cog(
            name="ratings",
            output=lambda: {
                1: {
                    "rating": 1507.5,
                    "gp": 1,
                },
                2: {
                    "rating": 1492.5,
                    "gp": 1,
                }
            }
        ))
        self.wheel.add(NormedRatingsCog(
            name="nratings",
            inputs=["ratings"],
        ))

        cog = Cog("check", inputs=["nratings"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
            1: 53.75,
            2: 46.25,
        })
