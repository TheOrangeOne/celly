from datetime import datetime, timedelta
from functools import reduce

from celly.cog import Cog
from celly.nhl import API
from celly.web import get_json

"""
The API is pretty straightforward and returns generally sensible data.

Doing a GET between two dates will return the schedule data for each day
between the two dates (inclusive).

The schema is roughly the following:

totalItems: ,
totalEvents: ,
totalGames: ,
totalMatches: ,
wait: ,
dates: [
  # list of schedule
  {
    date: "%Y-%m-%d",
    totalItems: ,
    totalEvents: ,
    totalGames: ,
    totalMatches: ,
    games: [
      # list of game
      {
        gameType: "R",  # regular season?
        season: "20182019",
        gameDate: "2018-10-13T17:00:00Z"
        status: {
          abstractGameState: "Preview",
          codedGameState: "1",
          detailedState: "Scheduled",
          statusCode: "1",
          startTimeTBD: false
        },
        teams: {
          away: {
            leagueRecord: {
              wins: 0,
              losses: 2,
              ot: 0,
              type: "league",
            },
            score: 0,
            team: {
              id: 22,
              name: "Edmonton Oilers",
              link: "/api/v1/teams/22"
            },
          },
          home: {}, # same format as away
       },
       linescore: {
         currentPeriod: 0,
         periods: [ ],
         shootoutInfo: {}, # not relevant (for now)
         teams: {
           home: {
             team: {} # same as team above
             goals: 0,
             shotsOnGoal: 0,
             goaliePulled: false,
             numSkaters: 0,
             powerPlay: false,
           },
           away: {}, # similar as home

The only edge case is when there is a day with _no_ games scheduled, then the
API returns _nothing_ in the "dates" field.
"""

class ScheduleUpdateCog(Cog):
    DATE_F         = "%Y-%m-%d"
    SEASON_START_F = "2018-10-03"
    SEASON_START   = datetime.strptime(SEASON_START_F, DATE_F)

    def _fetch_data(self, start, end):
        endpoint = "schedule?startDate={}&endDate={}&expand=schedule.linescore"
        endpoint = endpoint.format(start, end)
        url = "{}{}".format(API, endpoint)
        r = get_json(url)
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
            day = season_start + timedelta(days=day_i)
            day_f = day.strftime(self.DATE_F)

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

    def _last_update(self, sched):
        last_update_f = self.SEASON_START_F
        if len(sched):
            # check each of the day schedules to make sure they completed
            for day in sched:
                if not self._is_day_complete(day):
                    last_update_f = day["date"]
                    break
        else:
            last_update_f = self.SEASON_START_F

        return last_update_f

    def output(self, cached_sched):
        if not cached_sched:
            cached_sched = []

        now = datetime.now()
        now_f = now.strftime(self.DATE_F)

        last_update_f = self._last_update(cached_sched)
        last_update = datetime.strptime(last_update_f, self.DATE_F)

        if last_update >= now:
            return cached_sched

        new_sched_data = self._fetch_data(last_update_f, now_f)
        sched = self._merge_new_schedule(cached_sched, new_sched_data)
        sched = self._sanitize_schedule(sched, self.SEASON_START, now)
        return sched
