import copy

from celly.cog import Cog
from celly.web import get_json


class RedditUpdateTopCog(Cog):
    API = "https://reddit.com/r/hockey/top/.json?count={}"

    def get_top_for_day(self, num):
        url = self.API.format(num)
        return get_json(url)

    def merge_new(self, cached, new, date):
        merged = copy.deepcopy(cached)
        merged[date] = new["data"]["children"]
        return merged

    def output(self, cached_top, date):
        cached = cached_top or {}
        if date in cached:
            return cached

        new_top = self.get_top_for_day(10)
        top = self.merge_new(cached, new_top, date)
        return top
