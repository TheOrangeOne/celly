from celly.date import next_ymd, prev_ymd
from celly.cog import Cog
from celly.cogs.teams import get_id_abbr
from celly.file import File
from celly.pages import env
from celly.pages.ratings import ratings_page
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
            for game in games:
                teams = game["teams"]
                period = game["linescore"]["currentPeriod"]

                hid, hscore = get_team_id_score(teams["home"])
                aid, ascore = get_team_id_score(teams["away"])
                model.calculate_rating((hid, hscore), (aid, ascore), period)
            ratings_by_day[date] = model.copyratings()

        return ratings_by_day


def day_ratings(ratings, prev_ratings, teams):
    ratings_for_day = []
    for id, rating in ratings.items():
        abbr = get_id_abbr(teams, id)
        prev_rating = prev_ratings.get(id, {
            "rating": 1500.0,
        })
        diff = rating["rating"] - prev_rating["rating"]
        ratings_for_day.append(dict(
            abbr=abbr,
            rating=rating["rating"],
            diff=diff,
        ))
    ratings_for_day = sorted(
        ratings_for_day,
        key=lambda r: r["rating"],
        reverse=True
    )
    return ratings_for_day


class RenderRatingsByDayCog(Cog):
    """
    Input: RatingsByDay data
    Output: list of File for each day
    """
    def output(self, ratings_by_day, teams):
        pages = []
        prev_ratings = {}
        for date, ratings in ratings_by_day.items():
            ratings_for_day = day_ratings(ratings, prev_ratings, teams)
            temp = env.get_template("ratings.jinja2")
            r = temp.render(
                date=date,
                teams=teams,
                day_ratings=ratings_for_day,
            )
            page = File(
                name=ratings_page(date),
                src=r,
            )
            pages.append(page)
            prev_ratings = ratings

        return pages
