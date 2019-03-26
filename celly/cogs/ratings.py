import os

import matplotlib.pyplot as plt

from celly.date import next_ymd, prev_ymd
from celly.cog import Cog
from celly.cogs.teams import get_id_abbr, team_img
from celly.file import File
from celly.pages import env
from celly.pages.ratings import ratings_page
from celly.pages.team import team_rating_graph, team_rating_graph_icon
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

    def __call__(self, days, teams):
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
    def __call__(self, ratings):
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
            svg=team_img(id),
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
    def __call__(self, ratings_by_day, teams):
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


def gen_team_rating_graph(id, ratings, directory):
    team_ratings_by_date = {}
    dates = []
    team_ratings = []
    plt.xticks(rotation=270)
    for date, rating in ratings.items():
        team_rating = rating[id]
        dates.append(date)
        r = normalize_rating(team_rating["rating"])
        team_ratings.append(r)
    l = plt.plot(dates, team_ratings, 'ro-',  label='line 2')
    # for teams page
    path = os.path.join(directory, team_rating_graph(id))
    plt.savefig(path, bbox_inches = "tight")
    # for icon
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.setp(l, linewidth=12, color='r')
    path = os.path.join(directory, team_rating_graph_icon(id))
    plt.savefig(path)
    plt.clf()


class TeamRatingsGraphsCog(Cog):
    def __call__(self, teams, ratings, directory, enabled=True):
        if not enabled:
            return

        for id, team in teams.items():
            gen_team_rating_graph(id, ratings, directory)
