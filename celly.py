import os

from celly.cog import Cog, PrintCog
from celly.cogs.file import ReadJSONFileCog, WriteJSONFileCog
from celly.cogs.schedule import ScheduleUpdateCog
from celly.cogs.games import GamesCog, CompletedRegSeasonGamesCog
from celly.cogs.ratings import RatingsCog
from celly.cogwheel import CogWheel

DATA_DIR = os.path.join(os.getcwd(), "data/")
SCHED_FILE = os.path.join(DATA_DIR, "sched.json")


wheel = CogWheel()

wheel.add(Cog(
    name="sched_data_file",
    output=lambda: SCHED_FILE,
))

wheel.add(Cog(
    name="current_season",
    output=lambda: "20182019",
))

wheel.add(ReadJSONFileCog(
    name="raw_sched_data",
    inputs=["sched_data_file"]
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

wheel.add(RatingsCog(
    name="current_season_ratings",
    inputs=["current_season_completed_games"]
))

wheel.add(WriteJSONFileCog(
    inputs=["sched_data_file", "schedule"]
))

wheel.add(PrintCog(
    inputs=["current_season_ratings"]
))

wheel.start()
