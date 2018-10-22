from datetime import datetime

from celly.cog import Cog
from celly.cogs.teams import get_id_abbr, team_svg
from celly.date import next_ymd, prev_ymd
from celly.file import File
from celly.pages import env
from celly.pages.matches import match_page

def get_scores(game):
    teams = game["teams"]
    return teams["away"]["score"], teams["home"]["score"]


def get_match(game, teams):
    home = dict(game["teams"]["home"]["team"])
    hid = home["id"]
    away = dict(game["teams"]["away"]["team"])
    aid = away["id"]
    game_date = game["gameDate"]

    ascore, hscore = get_scores(game)
    home["abbr"] = get_id_abbr(teams, hid)
    home["svg"] = team_svg(hid)
    home["score"] = hscore
    away["abbr"] = get_id_abbr(teams, aid)
    away["svg"] = team_svg(aid)
    away["score"] = ascore

    period = game["linescore"]["currentPeriod"]
    if period == 4:
        period = "OT"
    elif period == 5:
        period = "SO"
    else:
        period = "RG"

    date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ")
    date = date.strftime("%H:%M")

    return dict(
        done=game["status"]["abstractGameState"] == "Final",
        home=home,
        away=away,
        date=date,
        period=period,
    )


class RenderDayMatchesCog(Cog):
    """
    Input: schedule
    Output: list of File representing rendered day matches
    """

    def output(self, sched, teams):
        days = []
        temp = env.get_template("matches.jinja2")
        dates = [day["date"] for day in sched]

        def get_page(date):
            return match_page(date) if date in dates else ''

        match_pages = []
        for day in sched:
            date = day["date"]

            matches = []
            for game in day["games"]:
                if game["gameType"] != "R":
                    continue
                matches.append(get_match(game, teams))

            r = temp.render(
                date=date,
                matches=matches,
                next_page=get_page(next_ymd(date)),
                prev_page=get_page(prev_ymd(date)),
            )
            page = File(
                name=match_page(date),
                src=r,
            )
            match_pages.append(page)
        return match_pages
