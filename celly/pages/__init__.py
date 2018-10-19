import datetime
from jinja2 import Environment, PackageLoader

from celly.date import next_ymd, prev_ymd
from .ratings import format_rating, format_diff, ratings_page

env = Environment(
    loader=PackageLoader("celly", "pages"),
)
env.globals["now"] = datetime.datetime.now().strftime("%c")
env.globals["next_ymd"] = next_ymd
env.globals["prev_ymd"] = prev_ymd
env.globals["format_rating"] = format_rating
env.globals["format_diff"] = format_diff
env.globals["ratings_page"] = ratings_page
