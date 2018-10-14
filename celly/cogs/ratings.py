from celly.cog import Cog
from celly.pages import env
from celly.rating import RatingModel, normalize_rating


class RatingsCog(Cog):
    """Cog for generating ratings.

    Input: list of games completed games

    Output: ratings by date grouped by team id
    """

    def output(self, days):
        model = RatingModel()
        ratings = {}
        for date, games in days.items():
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

                for id in [hid, aid]:
                    if date not in ratings:
                        ratings[date] = {}
                    ratings[date][id] = dict(model.ratings[id])

        return ratings


class RenderRatingsCog(Cog):
    def output(self, ratings_by_day):
        pages = []
        rating_changes = []
        for date, updates in ratings_by_day.items():
            for id, update in updates.items():
                rating_changes.append({
                    "id": id,
                    "rating": update["rating"],
                    "diff": update["diff"],
                })
            temp = env.get_template("ratings.html")
            r = temp.render(
                date=date,
                rating_changes=rating_changes,
            )
            pages.append(r)

        return pages
