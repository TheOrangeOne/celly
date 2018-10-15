from celly.cog import Cog
from celly.file import File
from celly.pages import env
from celly.rating import RatingModel, normalize_rating


def get_team_id_score(team):
    id = team["team"]["id"]
    score = team["score"]
    return id, score


class TeamRatingsByDayCog(Cog):
    """Cog for generating ratings.

    Input: list of games completed games

    Output: ratings by date grouped by team id
    """

    def output(self, days, teams):
        model = RatingModel(teams)
        ratings_by_day = {}
        for date, games in days.items():
            # clear out the diffs before each team for the day
            model.clear_diffs()

            for game in games:
                teams = game["teams"]
                period = game["linescore"]["currentPeriod"]

                hid, hscore = get_team_id_score(teams["home"])
                aid, ascore = get_team_id_score(teams["away"])
                model.calculate_rating((hid, hscore), (aid, ascore), period)
            ratings_by_day[date] = model.copyratings()

        return ratings_by_day


class RenderRatingsByDayCog(Cog):
    """
    Input: RatingsByDay data
    Output: list of File for each day
    """
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
            temp = env.get_template("ratings.jinja2")
            r = temp.render(
                date=date,
                rating_changes=rating_changes,
            )
            name = "{}-ratings.html".format(date)
            page = File(
                name=name,
                src=r,
            )
            pages.append(page)

        return pages
