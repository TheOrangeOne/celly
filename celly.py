import os

from celly.cog import Cog, PrintCog
from celly.cogs.file import ReadJSONFileCog, WriteJSONFileCog
from celly.cogs.schedule import ScheduleUpdateCog
from celly.cogwheel import CogWheel

DATA_DIR = os.path.join(os.getcwd(), "data/")
SCHED_FILE = os.path.join(DATA_DIR, "sched.json")


wheel = CogWheel()

wheel.add(Cog(
    name="sched_data_file",
    output=lambda: SCHED_FILE,
))

wheel.add(ReadJSONFileCog(
    name="raw_sched_data",
    inputs=["sched_data_file"]
))

wheel.add(ScheduleUpdateCog(
    name="sched_data",
    inputs=["raw_sched_data"]
))

wheel.add(WriteJSONFileCog(
    inputs=["sched_data_file", "sched_data"]
))

wheel.start()
