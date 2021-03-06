import datetime
from jinja2 import Environment, PackageLoader

from celly.date import next_ymd, prev_ymd
from .matches import match_page
from .digest import digest_page
from .ratings import format_rating, format_diff, ratings_page, rating_rgb, diff_rgb
from .team import team_page, team_rating_graph, team_rating_graph_icon

env = Environment(
    loader=PackageLoader("celly", "pages"),
)
now = datetime.datetime.now()
env.globals["now"] = now.strftime("%c")
env.globals["nowf"] = now.strftime("%Y-%m-%d")
env.globals["next_ymd"] = next_ymd
env.globals["prev_ymd"] = prev_ymd
env.globals["format_rating"] = format_rating
env.globals["format_diff"] = format_diff
env.globals["ratings_page"] = ratings_page
env.globals["match_page"] = match_page
env.globals["team_page"] = team_page
env.globals["team_rating_graph"] = team_rating_graph
env.globals["team_rating_graph_icon"] = team_rating_graph_icon
env.globals["digest_page"] = digest_page
env.globals["rating_rgb"] = rating_rgb
env.globals["diff_rgb"] = diff_rgb
