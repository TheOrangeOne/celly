from celly.cog import Cog
from celly.cogs.team import TeamRenderCog

from ..cog_utils import TestCase, TestCog


EXAMPLE_TEAMS_OUTPUT = {
    16: {
        "id": 16,
        "name": "Chicago Blackhawks",
        "venue": {
            "id": 5092,
            "name": "United Center",
            "city": "Chicago",
            "timeZone": {
                "id": "America/Chicago",
                "offset": -5,
                "tz": "CDT"
            }
        },
        "abbreviation": "CHI",
        "teamName": "Blackhawks",
        "locationName": "Chicago",
        "firstYearOfPlay": "1926",
        "division": {
            "id": 16,
            "name": "Central",
            "nameShort": "CEN",
            "abbreviation": "C"
        },
        "conference": {
            "id": 5,
            "name": "Western",
        },
        "franchise": {
            "franchiseId": 11,
            "teamName": "Blackhawks",
        },
        "shortName": "Chicago",
        "officialSiteUrl": "http://www.chicagoblackhawks.com",
        "franchiseId": 11,
    },
    30: {
        "id": 30,
        "name": "Minnesota Wild",
        "venue": {
            "id": 5098,
            "name": "Xcel Energy Center",
            "city": "St. Paul",
            "timeZone": {
                "id": "America/Chicago",
                "offset": -5,
                "tz": "CDT"
            }
        },
        "abbreviation": "MIN",
        "teamName": "Wild",
        "locationName": "Minnesota",
        "firstYearOfPlay": "1997",
        "division": {
            "id": 16,
            "name": "Central",
            "nameShort": "CEN",
            "abbreviation": "C"
        },
        "conference": {
            "id": 5,
            "name": "Western",
        },
        "franchise": {
            "franchiseId": 37,
            "teamName": "Wild",
        },
        "shortName": "Minnesota",
        "officialSiteUrl": "http://www.wild.com",
        "franchiseId": 37,
    }
}


class TestTeamRenderCog(TestCase):
    def test_sanity(self):
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
