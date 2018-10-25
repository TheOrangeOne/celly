from celly.cog import Cog
from celly.cogs.team import TeamRenderCog

from ..cog_utils import TestCase, TestCog


class TestTeamRenderCog(TestCase):
    def test_basic(self):
        self.wheel.add(Cog(
            name="teams",
            output=lambda: {
                "1": {
                    "abbreviation": "NJD",
                }
            }
        ))
        self.wheel.add(TeamRenderCog(
            name="pages",
            inputs=dict(
                teams="teams",
            )
        ))
        testcog = TestCog(
            inputs=dict(pages="pages")
        )

        self.wheel.add(testcog)
        self.wheel.start()
