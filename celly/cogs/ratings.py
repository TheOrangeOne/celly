from celly.date import next_ymd, prev_ymd
from celly.cog import Cog
from celly.cogs.teams import get_id_abbr, team_svg
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


class TeamDiffsByDayCog(Cog):
    """
    Input: ratings by day

    Output: rating diff by day
    """
    def output(self, ratings):
        diffs = {}
        for date, day_ratings in ratings.items():
            prev_date = prev_ymd(date)
            prev_day_ratings = ratings.get(prev_date, {})
            diffs[date] = {}
            for tid, rating in day_ratings.items():
                prev_rating = prev_day_ratings.get(tid, {})
                nr = normalize_rating(rating["rating"])
                pnr = normalize_rating(prev_rating.get("rating", 1500.0))
                diff = nr - pnr
                diffs[date][tid] = diff
        return diffs


def day_ratings(ratings, prev_ratings, teams):
    ratings_for_day = []
    for id, rating in ratings.items():
        abbr = get_id_abbr(teams, id)
        prev_rating = prev_ratings.get(id, {
            "rating": 1500.0,
        })
        nrating = normalize_rating(rating["rating"])
        pnrating = normalize_rating(prev_rating["rating"])
        diff = nrating - pnrating
        ratings_for_day.append(dict(
            abbr=abbr,
            diff=diff,
            rating=nrating,
            svg=team_svg(id),
        ))
    ratings_for_day = sorted(
        ratings_for_day,
        key=lambda r: r["rating"],
        reverse=True
    )
    return ratings_for_day


class RenderDayRatingsCog(Cog):
    """
    Input: RatingsByDay data
    Output: list of File for each day
    """
    def output(self, ratings_by_day, teams):
        pages = []
        prev_ratings = {}
        temp = env.get_template("ratings.jinja2")

        def get_page(date):
            return ratings_page(date) if date in ratings_by_day else ''

        for date, ratings in ratings_by_day.items():
            ratings_for_day = day_ratings(ratings, prev_ratings, teams)
            r = temp.render(
                date=date,
                teams=teams,
                day_ratings=ratings_for_day,
                next_page=get_page(next_ymd(date)),
                prev_page=get_page(prev_ymd(date)),
            )
            page = File(
                name=ratings_page(date),
                src=r,
            )
            pages.append(page)
            prev_ratings = ratings

        return pages
