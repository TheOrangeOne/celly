from celly.cog import Cog
from celly.rating import RatingModel, normalize_rating


class RatingsCog(Cog):
    """Cog for generating ratings.

    Input: list of games completed games

    Output: ratings grouped by team id
    """

    def output(self, games):
        model = RatingModel()

        for game in games:
            linescore = game["linescore"]
            teams = game["teams"]
            period = linescore["currentPeriod"]

            home = teams["home"]
            hid = home["team"]["id"]
            hscore = home["score"]

            away = teams["away"]
            aid = away["team"]["id"]
            ascore = away["score"]

            model.calculate_rating((hid, hscore), (aid, ascore), period)
        return model.ratings

 
class NormedRatingsCog(Cog):
    """Cog for normalizing ratings.

    Input: ratings dict output by RatingsCog

    Output: ratings dict with normalized ratings
    """

    def output(self, ratings):
        normedratings = {}
        for id, data in ratings.items():
            nrating = normalize_rating(data["rating"])
            normedratings[id] = nrating
        return normedratings
