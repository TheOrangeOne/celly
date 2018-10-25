from celly.cog import Cog
from celly.cogs.matches import RenderDayMatchesCog

from ..cog_utils import TestCase, TestCog
from .test_schedule import EXAMPLE_SCHED_OUTPUT
# from .test_ratings import EXAMPLE_RATINGS_OUTPUT
from .test_team import EXAMPLE_TEAMS_OUTPUT


EXAMPLE_RATINGS_OUTPUT = {
    "2018-10-10": {
        16: {
            "rating": 1500.00,
        },
        30: {
            "rating": 1500.00,
        }
    },
    "2018-10-11": {
        16: {
            "rating": 1500.00,
        },
        30: {
            "rating": 1500.00,
        }
    },
    "2018-10-12": {
        16: {
            "rating": 1500.00,
        },
        30: {
            "rating": 1500.00,
        }
    }
}

EXAMPLE_DIFFS_OUTPUT = {
    "2018-10-10": {
        16: 0.0,
        30: 0.0,
    },
    "2018-10-11": {
        16: 2.0,
        30: -2.0,
    },
    "2018-10-12": {
        16: 0.0,
        30: 0.0,
    }
}


class TestRenderDayMatchesCog(TestCase):
    def test_basic(self):
        self.wheel.add(Cog(
            name="sched",
            output=lambda: EXAMPLE_SCHED_OUTPUT,
        ))
        self.wheel.add(Cog(
            name="ratings",
            output=lambda: EXAMPLE_RATINGS_OUTPUT,
        ))
        self.wheel.add(Cog(
            name="teams",
            output=lambda: EXAMPLE_TEAMS_OUTPUT,
        ))
        self.wheel.add(Cog(
            name="diffs",
            output=lambda: EXAMPLE_DIFFS_OUTPUT,
        ))
        self.wheel.add(RenderDayMatchesCog(
            name="pages",
            inputs=dict(
                sched="sched",
                ratings="ratings",
                teams="teams",
                diffs="diffs",
            )
        ))
        testcog = TestCog(
            inputs=dict(pages="pages")
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()
