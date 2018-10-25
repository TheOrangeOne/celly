from celly.cog import Cog
from celly.cogs.ratings import TeamRatingsByDayCog, RenderDayRatingsCog

from ..cog_utils import TestCog, TestCase


class TestRatingsCog(TestCase):
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
            }
        ))

        self.wheel.add(TeamRatingsByDayCog(
            name="ratings",
            inputs=dict(
                days="games",
                teams="teams",
            ),
        ))

        testcog = TestCog(
            inputs=dict(
                ratings="ratings",
            ),
            should_be_called_with=dict(
                ratings={
                    "2018-10-12": {
                        1: {
                            "rating": 1500.0,
                            "gp": 0,
                        },
                        2: {
                            "rating": 1500.0,
                            "gp": 0,
                        },
                    },
                    "2018-10-13": {
                        1: {
                            "rating": 1507.5,
                            "gp": 1,
                        },
                        2: {
                            "rating": 1492.5,
                            "gp": 1,
                        },
                    },
                    "2018-10-14": {
                        1: {
                            "rating": 1507.5,
                            "gp": 1,
                        },
                        2: {
                            "rating": 1492.5,
                            "gp": 1,
                        },
                    },
                    "2018-10-15": {
                        1: {
                            "rating": 1514.6764000042328,
                            "gp": 2,
                        },
                        2: {
                            "rating": 1485.3235999957672,
                            "gp": 2,
                        },
                    }
                }
            ),
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    def test_render_page(self):
        self.wheel.add(Cog(
            name="teams",
            output=lambda: {
                1: {
                    "abbreviation": "TOR"
                },
                2: {
                    "abbreviation": "ANA"
                },
            }
        ))
        self.wheel.add(Cog(
            name="ratings",
            output=lambda: {
                "2018-10-13": {
                    1: {
                        "rating": 1507.5,
                        "gp": 1,
                    },
                    2: {
                        "rating": 1492.5,
                        "gp": 1,
                    },
                },
                "2018-10-14": {
                    1: {
                        "rating": 1514.6764000042328,
                        "gp": 2,
                    },
                    2: {
                        "rating": 1485.3235999957672,
                        "gp": 2,
                    },
                }
            }))
        self.wheel.add(RenderDayRatingsCog(
            name="render",
            inputs=dict(
                ratings_by_day="ratings",
                teams="teams",
            ),
        ))

        testcog = TestCog(
            inputs=dict(
                render="render",
            ),
        )
        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()
