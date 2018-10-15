import json
from urllib.request import urlopen


def get(url):
    print("GET {}".format(url))
    return urlopen(url).read()

def get_json(url):
    r = get(url)
    return json.loads(r)
