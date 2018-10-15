import os

from celly.cog import Cog, PrintCog
from celly.cogs.file import ReadJSONFileCog, WriteJSONFileCog, WriteFiles
from celly.cogs.schedule import ScheduleUpdateCog
from celly.cogs.games import GamesCog, CompletedRegSeasonGamesCog
from celly.cogs.ratings import TeamRatingsByDayCog, RenderRatingsByDayCog
from celly.cogs.teams import TeamsCog
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

wheel.add(GamesCog(
    name="all_games",
    inputs=["schedule"]
))


wheel.add(CompletedRegSeasonGamesCog(
    name="current_season_completed_games",
    inputs=["current_season", "all_games"]
))

wheel.add(TeamRatingsByDayCog(
    name="current_season_ratings_by_day",
    inputs=["current_season_completed_games", "teams"]
))

wheel.add(RenderRatingsByDayCog(
    name="rendered_current_season_ratings",
    inputs=["current_season_ratings_by_day"]
))

wheel.add(WriteFiles(
    inputs=[
        "rendered_current_season_ratings",
        "build_directory",
    ]
))

wheel.add(WriteJSONFileCog(
    inputs=["teams_data_file", "teams", "data_directory"]
))

wheel.add(WriteJSONFileCog(
    inputs=["sched_data_file", "schedule", "data_directory"]
))

wheel.add(PrintCog(
    inputs=[""]
))

wheel.start()
