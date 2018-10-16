from celly.cog import Cog
from celly.nhl import API
from celly.web import get_json



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

    def output(self, cached_teams):
        if cached_teams:
            return self.get_cached_teams(cached_teams)
        raw_teams = self.get_raw_teams()
        teams = self.get_teams(raw_teams)
        return teams
