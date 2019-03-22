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
    TeamRatingsGraphsCog,
)
from celly.cogs.reddit import (
    RedditUpdateSubsTopCog,
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
    name="cached_sched_data",
    inputs=dict(
        filename="sched_data_file",
        directory="data_directory",
    ),
))

wheel.add(ReadJSONFileCog(
    name="cached_teams_data",
    inputs=dict(
        filename="teams_data_file",
        directory="data_directory",
    ),
))

wheel.add(ReadJSONFileCog(
    name="cached_reddit_top",
    inputs=dict(
        filename="reddit_top_data_file",
        directory="data_directory",
    ),
))

wheel.add(RedditUpdateSubsTopCog(
    name="reddit_top_by_date",
    inputs=dict(
        cached_top="cached_reddit_top",
        date="date_f"
    ),
))

wheel.add(TeamsCog(
    name="teams",
    inputs=dict(
        cached_teams="cached_teams_data"
    ),
))

wheel.add(Cog(
    name="FORCE_CACHE",
    output=lambda: not(os.environ.get("CELLY_FORCE_CACHE", "false") == "false"),
))

wheel.add(ScheduleUpdateCog(
    name="schedule",
    inputs=dict(
        cached_sched="cached_sched_data",
        fetch="FORCE_CACHE",
    ),
))

wheel.add(CompletedRegSeasonGamesCog(
    name="current_season_completed_games",
    inputs=dict(
        season_s="current_season",
        sched="schedule",
    ),
))

"""
Match cogs
"""
wheel.add(RenderDayMatchesCog(
    name="match_pages",
    inputs=dict(
        sched="schedule",
        teams="teams",
        ratings="current_season_ratings_by_day",
        diffs="current_season_diffs_by_day",
    ),
))

"""
Digest cogs
"""
wheel.add(RenderDayDigestCog(
    name="digest_pages",
    inputs=dict(
        sched="schedule",
        reddit_top="reddit_top_by_date",
    ),
))


"""
Ratings cogs
"""
wheel.add(TeamRatingsByDayCog(
    name="current_season_ratings_by_day",
    inputs=dict(
        days="current_season_completed_games",
        teams="teams",
    ),
))

wheel.add(TeamDiffsByDayCog(
    name="current_season_diffs_by_day",
    inputs=dict(
        ratings="current_season_ratings_by_day"
    ),
))

wheel.add(RenderDayRatingsCog(
    name="current_season_ratings_pages",
    inputs=dict(
        ratings_by_day="current_season_ratings_by_day",
        teams="teams",
    ),
))

"""
Team SVG cogs
"""

wheel.add(TeamsSVGCog(
    name="teams_svg_names",
    inputs=dict(
        teams="teams"
    ),
))

wheel.add(FilterFilesDNECog(
    name="missing_teams_svg_names",
    inputs=dict(
        files="teams_svg_names",
        directory="build_directory",
    ),
))

wheel.add(TeamsGetSVGCog(
    name="teams_svgs",
    inputs=dict(
        files="missing_teams_svg_names",
    ),
))

wheel.add(TeamRenderCog(
    name="team_pages",
    inputs=dict(
        teams="teams",
    ),
))

wheel.add(Cog(
    name="GENERATE_GRAPHS",
    output=lambda: os.environ.get("CELLY_GEN_GRAPHS", "true") == "true"))

wheel.add(TeamRatingsGraphsCog(
    name="team_rating_graphs",
    inputs=dict(
        teams="teams",
        ratings="current_season_ratings_by_day",
        directory="build_directory",
        enabled="GENERATE_GRAPHS"
    ),
))

"""
File persistence Cogs
"""
wheel.add(WriteFilesCog(
    inputs=dict(
        files="current_season_ratings_pages",
        directory="build_directory",
    ),
))

wheel.add(WriteFilesCog(
    inputs=dict(
        files="match_pages",
        directory="build_directory",
    ),
))

wheel.add(WriteFilesCog(
    inputs=dict(
        files="team_pages",
        directory="build_directory",
    ),
))

wheel.add(WriteFilesCog(
    inputs=dict(
        files="digest_pages",
        directory="build_directory",
    ),
))

wheel.add(WriteFilesCog(
    inputs=dict(
        files="teams_svgs",
        directory="build_directory",
    ),
))


wheel.add(WriteJSONFileCog(
    inputs=dict(
        filename="teams_data_file",
        data="teams",
        directory="data_directory",
    ),
))

wheel.add(WriteJSONFileCog(
    inputs=dict(
        filename="sched_data_file",
        data="schedule",
        directory="data_directory",
    ),
))

wheel.add(WriteJSONFileCog(
    inputs=dict(
        filename="reddit_top_data_file",
        data="reddit_top_by_date",
        directory="data_directory",
    ),
))

# wheel.add(PrintCog(
#     inputs=dict(_=""),
# ))

wheel.start()
