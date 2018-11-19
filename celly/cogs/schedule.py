import datetime
from functools import reduce

from celly.date import FMT
from celly.cog import Cog
from celly.nhl import API
import celly.web

"""
See test_schedule.py for what the API returns.

The only edge case is when there is a day with _no_ games scheduled, then the
API returns _nothing_ in the "dates" field.
"""

class ScheduleUpdateCog(Cog):
    def _fetch_data(self, start, end):
        endpoint = "schedule?startDate={}&endDate={}&expand=schedule.linescore"
        endpoint = endpoint.format(start, end)
        url = "{}{}".format(API, endpoint)
        r = celly.web.get_json(url)
        return r

    def _merge_new_schedule(self, old_sched, new_sched_data):
        """Merges a schedule with new data obtained from the API.
        """
        if not new_sched_data or "dates" not in new_sched_data:
            return old_sched
        dates = new_sched_data["dates"]

        if not dates:
            return old_sched

        combined_sched = []
        first_new_date = dates[0]["date"]
        for date in old_sched:
            if date["date"] == first_new_date:
                return combined_sched + dates
            else:
                combined_sched.append(date)

        return combined_sched + dates

    def _sanitize_schedule(self, sched, season_start, now):
        """Sanitizes the schedule data.

        Loops over each day since the season start to present and checks that
        there is an entry for the day.
        """
        sanitized_sched = []
        ndays = (now - season_start).days + 1

        sched_i = 0

        for day_i in range(0, ndays):
            day = season_start + datetime.timedelta(days=day_i)
            day_f = day.strftime(FMT)

            if sched_i >= len(sched) or "date" not in sched[sched_i] or sched[sched_i]["date"] != day_f:
                sanitized_sched.append({
                    "date": day_f,
                    "totalGames": 0,
                    "games": []
                })
            else:
                day_sched = sched[sched_i]
                sanitized_sched.append(day_sched)
                sched_i += 1

        return sanitized_sched

    def _is_day_complete(self, day):
        if day["totalGames"] == 0:
            return True
        return reduce(lambda x, y: x and y, map(self._is_game_complete, day["games"]))

    def _is_game_complete(self, game):
        return game["status"]["abstractGameState"] == "Final"

    def _last_update(self, sched, season_start_f):
        last_update_f = season_start_f
        if len(sched):
            # check each of the day schedules to make sure they completed
            for day in sched:
                if not self._is_day_complete(day):
                    last_update_f = day["date"]
                    break
        else:
            last_update_f = season_start_f

        return last_update_f

    def __call__(self, cached_sched, fetch=True, now=None, season_start="2018-10-03"):
        season_start_f = season_start
        season_start = datetime.datetime.strptime(season_start_f, FMT)
        if not cached_sched:
            cached_sched = []

        if not fetch:
            return cached_sched

        if not now:
            now = datetime.datetime.now()
        now_f = now.strftime(FMT)

        last_update_f = self._last_update(cached_sched, season_start_f)
        last_update = datetime.datetime.strptime(last_update_f, FMT)

        if last_update >= now:
            return cached_sched

        new_sched_data = self._fetch_data(last_update_f, now_f)
        sched = self._merge_new_schedule(cached_sched, new_sched_data)
        sched = self._sanitize_schedule(sched, season_start, now)
        return sched
