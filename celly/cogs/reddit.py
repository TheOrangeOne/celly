import copy
import logging

from celly.cog import Cog
from celly.web import get_reddit


log = logging.getLogger(__name__)


class RedditUpdateTopCog(Cog):
    API = "r/hockey/top/.json?count={}"

    def get_top_for_day(self, num):
        url = self.API.format(num)
        try:
            top = get_reddit(url)
        except Exception:
            top = None
            log.error("failed to get reddit top posts")
        return top

    def merge_new(self, cached, new, date):
        merged = copy.deepcopy(cached)
        merged[date] = new["data"]["children"]
        return merged

    def output(self, cached_top, date):
        cached = cached_top or {}
        if date in cached:
            return cached

        new_top = self.get_top_for_day(10)
        if new_top:
            top = self.merge_new(cached, new_top, date)
            return top
        return cached
