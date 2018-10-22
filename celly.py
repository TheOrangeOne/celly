import os

from celly.cog import Cog, PrintCog
from celly.cogs.file import (
    FilterFilesDNECog,
    ReadJSONFileCog,
    WriteJSONFileCog,
    WriteFilesCog,
)
from celly.cogs.games import CompletedRegSeasonGamesCog
from celly.cogs.matches import RenderDayMatchesCog
from celly.cogs.ratings import (
    RenderRatingsByDayCog,
    TeamRatingsByDayCog,
)
from celly.cogs.team import TeamRenderCog
from celly.cogs.teams import (
    TeamsCog,
    TeamsGetSVGCog,
    TeamsSVGCog,
)
from celly.cogs.schedule import ScheduleUpdateCog
from celly.cogwheel import CogWheel


CWD = os.getcwd()
DATA_DIR = os.path.join(CWD, "data/")
BUILD_DIR = os.path.join(CWD, "build/")


wheel = CogWheel()

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


wheel.add(ReadJSONFileCog(
    name="raw_sched_data",
    inputs=["sched_data_file", "data_directory"]
))

wheel.add(ReadJSONFileCog(
    name="raw_teams_data",
    inputs=["teams_data_file", "data_directory"]
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
    inputs=["schedule", "teams", "current_season_ratings_by_day"]
))


"""
Ratings cogs
"""
wheel.add(TeamRatingsByDayCog(
    name="current_season_ratings_by_day",
    inputs=["current_season_completed_games", "teams"]
))

wheel.add(RenderRatingsByDayCog(
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
        "teams_svgs",
        "build_directory",
    ]
))

wheel.add(WriteJSONFileCog(
    inputs=["teams_data_file", "teams", "data_directory"]
))

wheel.add(WriteJSONFileCog(
    inputs=["sched_data_file", "schedule", "data_directory"]
))

# wheel.add(PrintCog(
#     inputs=["current_season_completed_games"]
# ))

wheel.start()
