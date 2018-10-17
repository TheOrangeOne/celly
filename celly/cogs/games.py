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
            for game in day["games"]:
                games.append(game)
        return games


class CompletedRegSeasonGamesCog(Cog):
    """Cog for getting only completed games for the current season.
    """
    def output(self, season_s, sched):
        def completed_reg_season(game):
            s = game["season"] == season_s
            t = game["gameType"] == "R"
            c = game["status"]["abstractGameState"] == "Final"
            return s and t and c

        season = {}
        for day in sched:
            date = day["date"]
            if date not in season:
                season[date] = []
            if day["totalGames"] == 0:
                continue

            for game in day["games"]:
                if not completed_reg_season(game):
                    continue
                season[date].append(game)

        return season
