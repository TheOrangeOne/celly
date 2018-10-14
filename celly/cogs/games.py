from celly.cog import Cog

class GamesCog(Cog):
    """Cog for game data.

    Input: schedule of game data

    Output: flattened list of all games in the schedule
    """

    def output(self, sched):
        games = []
        for day in sched:
            if day["totalGames"] == 0:
                continue
            games += day["games"]

        return games


class CompletedRegSeasonGamesCog(Cog):
    """Cog for getting only completed games for the current season.
    """
    def output(self, season, games):
        def completed_reg_season(game):
            s = game["season"] == season
            t = game["gameType"] == "R"
            c = game["status"]["abstractGameState"] == "Final"
            return s and t and c

        games = list(filter(completed_reg_season, games))

        season = {}
        for game in games:
            date = game["gameDate"][0:10]
            if date not in season:
                season[date] = []
            season[date].append(game)

        return season
