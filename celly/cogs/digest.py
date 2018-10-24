from celly.cog import Cog

from datetime import datetime

from celly.cog import Cog
from celly.cogs.teams import get_id_abbr, team_svg
from celly.date import next_ymd, prev_ymd
from celly.file import File
from celly.pages import env
from celly.pages.digest import digest_page


class RenderDayDigestCog(Cog):
    """
    """
    "close_games, hot teams, etc"
    def __call__(self, sched, reddit_top):
        days = []
        temp = env.get_template("digest.jinja2")
        dates = [day["date"] for day in sched]

        def get_page(date):
            return digest_page(date) if date in dates else ''

        digest_pages = []
        for day in sched:
            date = day["date"]

            reddit_top_day = reddit_top.get(date, [])
            if len(reddit_top_day) > 5:
                reddit_top_day = reddit_top_day[0:5]

            r = temp.render(
                date=date,
                next_page=get_page(next_ymd(date)),
                prev_page=get_page(prev_ymd(date)),
                reddit_top=reddit_top_day
            )
            page = File(
                name=digest_page(date),
                src=r,
            )
            digest_pages.append(page)
        return digest_pages
