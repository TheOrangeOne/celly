import unittest.mock as mock

from celly.cog import Cog
from celly.cogs.teams import TeamsCog

from ..cog_utils import TestCog, TestCase


class TestTeamsCog(TestCase):
    def test_teams_cog_cached(self):
        self.wheel.add(Cog(
            name="raw_teams",
            output=lambda: {
            1: {
                "id": 1,
                "name": "New Jersey Devils",
                "abbreviation": "NJD",
            },
            2: {
                "id" : 2,
                "name" : "New York Islanders",
                "abbreviation" : "NYI",
            }}
        ))

        self.wheel.add(TeamsCog(
            name="teams",
            inputs=dict(
                cached_teams="raw_teams",
            ),
        ))

        testcog = TestCog(
            inputs=dict(
                teams="teams",
            ),
            should_be_called_with=dict(
                teams={
                    1: {
                        "id": 1,
                        "name": "New Jersey Devils",
                        "abbreviation": "NJD",
                    },
                    2: {
                        "id" : 2,
                        "name" : "New York Islanders",
                        "abbreviation" : "NYI",
                    }
                }),
        )
        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    def test_teams_cog_new(self):
        self.wheel.add(Cog(
            name="raw_teams",
            output=lambda: None
        ))

        teamscog = TeamsCog(
            name="teams",
            inputs=dict(
                cached_teams="raw_teams",
            ),
        )
        teamscog.get_raw_teams = mock.MagicMock(return_value={
            "teams": [{
                "id" : 1,
                "name": "New Jersey Devils",
            },{
                "id": 2,
                "name": "New York Islanders",
            }]
        })

        self.wheel.add(teamscog)

        testcog = TestCog(
            inputs=dict(
                teams="teams",
            ),
            should_be_called_with=dict(
                teams={
                    1: {
                        "id": 1,
                        "name": "New Jersey Devils",
                    },
                    2: {
                        "id" : 2,
                        "name" : "New York Islanders",
                    }
                }
            ),
        )
        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()
