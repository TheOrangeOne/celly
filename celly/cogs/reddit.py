import copy
import logging

from celly.cog import Cog
import celly.web


log = logging.getLogger(__name__)


class RedditUpdateSubsTopCog(Cog):
    API = "r/{}/top/.json?count={}"

    def get_top_for_day(self, sub, num):
        url = self.API.format(sub, num)
        try:
            top = celly.web.get_reddit(url)
        except Exception:
            top = None
            log.error("failed to get reddit top posts")
        return top

    def merge_new(self, cached, new, date):
        cached[date] = [post["data"] for post in new["data"]["children"]]
        return cached

    def __call__(self, cached_top, date, subs=["hockey"], num=20):
        cached = cached_top or {}

        new_tops = {}
        for sub in subs:
            new_tops[sub] = {}
            cache = copy.deepcopy(cached.get(sub, {}))
            if date in cache:
                new_tops[sub] = cache
                continue

            new_top = self.get_top_for_day(sub, num)
            if not new_top:
                continue
            new_top = self.merge_new(cache, new_top, date)
            new_tops[sub] = new_top
        return new_tops
