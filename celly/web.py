import json
import logging
import os
from urllib.request import Request, urlopen

import requests
import requests.auth


log = logging.getLogger(__name__)


def get(url):
    log.info("GET {}".format(url))
    return urlopen(url).read()


def get_json(url):
    r = get(url)
    return json.loads(r)


REDDIT_USER_AGENT = "linux:cellyhockeyapp:0.0"
REDDIT_TOKEN = None


def auth_reddit():
    id = os.getenv('CELLY_REDDIT_APP_ID', None)
    sec = os.getenv('CELLY_REDDIT_APP_SECRET', None)
    if not id or not sec:
        return None
    client_auth = requests.auth.HTTPBasicAuth(id, sec)
    post_data = {
        "grant_type": "client_credentials",
    }
    headers = {
        "User-Agent": REDDIT_USER_AGENT,
    }
    log.info("REDDIT AUTH")
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
    )
    r = response.json()
    REDDIT_TOKEN = r.get("access_token", None)


REDDIT_BASE = "https://reddit.com/{}"


def get_reddit(url):
    if not REDDIT_TOKEN:
        auth_reddit()

    headers = {
        "Authorization": "bearer {}".format(REDDIT_TOKEN),
        "User-Agent": REDDIT_USER_AGENT
    }
    url = REDDIT_BASE.format(url)
    log.info("GET {}".format(url))
    response = requests.get(url, headers=headers)
    rjson = response.json()
    return rjson
