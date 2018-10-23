import logging
import os

from celly.cog import Cog, PrintCog
from celly.cogs.digest import RenderDayDigestCog
from celly.cogs.file import (
    FilterFilesDNECog,
    ReadJSONFileCog,
    WriteJSONFileCog,
    WriteFilesCog,
)
from celly.cogs.games import CompletedRegSeasonGamesCog
from celly.cogs.matches import RenderDayMatchesCog
from celly.cogs.ratings import (
    RenderDayRatingsCog,
    TeamDiffsByDayCog,
    TeamRatingsByDayCog,
)
from celly.cogs.reddit import (
    RedditUpdateTopCog,
)
from celly.cogs.team import TeamRenderCog
from celly.cogs.teams import (
    TeamsCog,
    TeamsGetSVGCog,
    TeamsSVGCog,
)
from celly.cogs.schedule import ScheduleUpdateCog
from celly.cogwheel import CogWheel
from celly.date import DATE_F

logging.basicConfig(level=logging.INFO)

CWD = os.getcwd()
DATA_DIR = os.path.join(CWD, "data/")
BUILD_DIR = os.path.join(CWD, "build/")


wheel = CogWheel()

wheel.add(Cog(
    name="date_f",
    output=lambda: DATE_F,
))

wheel.add(Cog(
    name="current_season",
    output=lambda: "20182019",
))

wheel.add(Cog(
    name="data_directory",
    output=lambda: DATA_DIR,
))

wheel.add(Cog(
    name="build_directory",
    output=lambda: BUILD_DIR,
))

wheel.add(Cog(
    name="sched_data_file",
    output=lambda: "sched.json",
))

wheel.add(Cog(
    name="teams_data_file",
    output=lambda: "teams.json",
))

wheel.add(Cog(
    name="reddit_top_data_file",
    output=lambda: "reddit_top.json",
))


wheel.add(ReadJSONFileCog(
    name="raw_sched_data",
    inputs=["sched_data_file", "data_directory"]
))

wheel.add(ReadJSONFileCog(
    name="raw_teams_data",
    inputs=["teams_data_file", "data_directory"]
))

wheel.add(ReadJSONFileCog(
    name="raw_reddit_top",
    inputs=["reddit_top_data_file", "data_directory"]
))

wheel.add(RedditUpdateTopCog(
    name="reddit_top_by_date",
    inputs=["raw_reddit_top", "date_f"]
))

wheel.add(TeamsCog(
    name="teams",
    inputs=["raw_teams_data"]
))


wheel.add(ScheduleUpdateCog(
    name="schedule",
    inputs=["raw_sched_data"]
))

wheel.add(CompletedRegSeasonGamesCog(
    name="current_season_completed_games",
    inputs=["current_season", "schedule"]
))

"""
Match cogs
"""
wheel.add(RenderDayMatchesCog(
    name="match_pages",
    inputs=[
        "schedule",
        "teams",
        "current_season_ratings_by_day",
        "current_season_diffs_by_day",
    ]
))

"""
Digest cogs
"""
wheel.add(RenderDayDigestCog(
    name="digest_pages",
    inputs=["schedule", "reddit_top_by_date"]
))


"""
Ratings cogs
"""
wheel.add(TeamRatingsByDayCog(
    name="current_season_ratings_by_day",
    inputs=["current_season_completed_games", "teams"]
))

wheel.add(TeamDiffsByDayCog(
    name="current_season_diffs_by_day",
    inputs=["current_season_ratings_by_day"]
))

wheel.add(RenderDayRatingsCog(
    name="current_season_ratings_pages",
    inputs=["current_season_ratings_by_day", "teams"]
))

"""
Team SVG cogs
"""

wheel.add(TeamsSVGCog(
    name="teams_svg_names",
    inputs=["teams"]
))

wheel.add(FilterFilesDNECog(
    name="missing_teams_svg_names",
    inputs=["teams_svg_names", "build_directory"]
))

wheel.add(TeamsGetSVGCog(
    name="teams_svgs",
    inputs=["missing_teams_svg_names"]
))

wheel.add(TeamRenderCog(
    name="team_pages",
    inputs=["teams", "current_season_ratings_by_day"]
))



"""
File persistence Cogs
"""
wheel.add(WriteFilesCog(
    inputs=[
        "current_season_ratings_pages",
        "build_directory",
    ]
))

wheel.add(WriteFilesCog(
    inputs=[
        "match_pages",
        "build_directory",
    ]
))

wheel.add(WriteFilesCog(
    inputs=[
        "team_pages",
        "build_directory",
    ]
))

wheel.add(WriteFilesCog(
    inputs=[
        "digest_pages",
        "build_directory",
    ]
))

wheel.add(WriteFilesCog(
    inputs=[
        "teams_svgs",
        "build_directory",
    ]
))


wheel.add(WriteJSONFileCog(
    inputs=[
        "teams_data_file",
        "teams",
        "data_directory",
    ]
))

wheel.add(WriteJSONFileCog(
    inputs=[
        "sched_data_file",
        "schedule",
        "data_directory"
    ]
))

wheel.add(WriteJSONFileCog(
    inputs=[
        "reddit_top_data_file",
        "reddit_top_by_date",
        "data_directory",
    ]
))

wheel.add(PrintCog(
    inputs=[""]
))

wheel.start()
