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

class GamesBySeasonCog(Cog):
    """Cog for game data.

    Input: schedule of game data

    Output: games organized by season, match type and date
    """
    def _get_season(self, day):
        return day["games"][0]["season"]

    def output(self, sched):
        seasons = {}
        for day in sched:
            date = day["date"]
            if day["totalGames"] == 0:
                continue

            for game in day["games"]:
                game_type = game["gameType"]
                season = game["season"]
                if season not in seasons:
                    seasons[season] = {
                        "R": {},
                    }
                season = seasons[season]
                if game_type not in season:
                    seasons[game_type] = {}

                if date not in season[game_type]:
                    season[game_type][date] = []

                season[game_type][date].append(game)

        return seasons


class CompletedRegSeasonGamesCog(Cog):
    """Cog for getting only completed games for the current season.
    """
    def output(self, season, games):
        def completed_reg_season(game):
            s = game["season"] == season
            t = game["gameType"] == "R"
            c = game["status"]["abstractGameState"] == "Final"
            return s and t and c

        games = filter(completed_reg_season, games)
        return list(games)
