from celly.cog import Cog
from celly.file import File
from celly.nhl import API
from celly.web import get, get_json


def get_id_abbr(teams, id):
    return teams[id]["abbreviation"]


class TeamsCog(Cog):
    def get_raw_teams(self):
        endpoint = "teams"
        url = "{}{}".format(API, endpoint)
        raw_teams = get_json(url)
        return raw_teams

    def get_teams(self, raw_teams):
        raw_teams = raw_teams["teams"]
        teams = {}
        for team in raw_teams:
            id = team["id"]
            teams[id] = team
        return teams

    def get_cached_teams(self, cached_teams):
        teams = {}
        for team in cached_teams.values():
            id = team["id"]
            teams[id] = team
        return teams

    def __call__(self, cached_teams):
        if cached_teams:
            return self.get_cached_teams(cached_teams)
        raw_teams = self.get_raw_teams()
        teams = self.get_teams(raw_teams)
        return teams


class TeamsSVGCog(Cog):
    """
    Input: teams dict
    Output: list of svg files for each team
    """
    def __call__(self, teams):
        svgs = []
        for id in teams:
            svgs.append("{}.svg".format(id))
        return svgs


def team_svg(id):
    return "{}.png".format(id)


class TeamsGetSVGCog(Cog):
    """
    Input: list of svg files to get
    Output: list of svg files retrieved from NHL api
    """
    IMG_API_BASE = "https://www-league.nhlstatic.com/builds/si  te-core/86d4b76cc03a4d111ee0e20f9f62eb054eef3b74_1502985652/imag  es/logos/team/current/team-{}-dark.svg"
    def __call__(self, files):
        svgs = []
        for filename in files:
            id = filename.split('.')[0]
            endpoint = self.IMG_API_BASE.format(id)
            svg = get(endpoint)
            svgs.append(File(
                name=team_svg(id),
                src=svg,
            ))
        return svgs
