import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogwheel import CogWheel
from celly.cogs.teams import TeamsCog


class TestTeamsCog(unittest.TestCase):
    def setUp(self):
        self.wheel = CogWheel()

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
            inputs=["raw_teams"]
        ))

        cog = Cog("check", inputs=["teams"])
        cog.output = mock.Mock()
        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
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
        })

    def test_teams_cog_new(self):
        self.wheel.add(Cog(
            name="raw_teams",
            output=lambda: None
        ))

        teamscog = TeamsCog(
            name="teams",
            inputs=["raw_teams"]
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

        cog = Cog("check", inputs=["teams"])
        cog.output = mock.Mock()
        self.wheel.add(cog)
        self.wheel.start()
        cog.output.assert_called_once()
        cog.output.assert_called_with({
            1: {
                "id": 1,
                "name": "New Jersey Devils",
            },
            2: {
                "id" : 2,
                "name" : "New York Islanders",
            }
        })
