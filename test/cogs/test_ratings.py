import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogwheel import CogWheel
from celly.cogs.ratings import TeamRatingsByDayCog, RenderRatingsByDayCog


class TestRatingsCog(unittest.TestCase):
    def setUp(self):
        self.wheel = CogWheel()

    def test_ratings_basic(self):
        self.wheel.add(Cog(
            name="teams",
            output=lambda: {
                1: {},
                2: {},
            }
        ))
        self.wheel.add(Cog(
            name="games",
            output=lambda: {
                "2018-10-12": [],
                "2018-10-13": [{
                    "gameType": "R",
                    "gameDate": "2018-10-13T17:00:00Z",
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
                }],
                "2018-10-14": [],
                "2018-10-15": [{
                    "gameType": "R",
                    "gameDate": "2018-10-15T17:00:00Z",
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
                }],
            }))
        self.wheel.add(TeamRatingsByDayCog(
            name="ratings",
            inputs=["games", "teams"],
        ))

        cog = Cog("check", inputs=["ratings"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
            "2018-10-12": {
                1: {
                    "rating": 1500.0,
                    "gp": 0,
                    "diff": 0.0,
                },
                2: {
                    "rating": 1500.0,
                    "gp": 0,
                    "diff": 0.0,
                },
            },
            "2018-10-13": {
                1: {
                    "rating": 1507.5,
                    "gp": 1,
                    "diff": 7.5,
                },
                2: {
                    "rating": 1492.5,
                    "gp": 1,
                    "diff": -7.5,
                },
            },
            "2018-10-14": {
                1: {
                    "rating": 1507.5,
                    "gp": 1,
                    "diff": 0.0,
                },
                2: {
                    "rating": 1492.5,
                    "gp": 1,
                    "diff": 0.0,
                },
            },
            "2018-10-15": {
                1: {
                    "rating": 1514.6764000042328,
                    "gp": 2,
                    "diff": 7.176400004232846,
                },
                2: {
                    "rating": 1485.3235999957672,
                    "gp": 2,
                    "diff": -7.176400004232846,
                },
            }
        })

    def test_render_page(self):
        self.wheel.add(Cog(
            name="ratings",
            output=lambda: {
                1: {
                    "2018-10-13": {
                        "rating": 1507.5,
                        "gp": 1,
                        "diff": 7.5,
                    },
                    "2018-10-14": {
                        "rating": 1514.6764000042328,
                        "gp": 2,
                        "diff": 7.176400004232846,
                    }
                },
                2: {
                    "2018-10-13": {
                        "rating": 1492.5,
                        "gp": 1,
                        "diff": -7.5,
                    },
                    "2018-10-14": {
                        "rating": 1485.3235999957672,
                        "gp": 2,
                        "diff": -7.176400004232846,
                    }
                }
            }))
        self.wheel.add(RenderRatingsByDayCog(
            name="render",
            inputs=["ratings"],
        ))

        cog = Cog("check", inputs=["render"])
        cog.output = mock.Mock()

        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        # cog.output.assert_called_with([])
