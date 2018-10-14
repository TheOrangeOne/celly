import json


class Cache(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._data = None

    def load(self):
        with open(self._file_name) as f:
            data = json.load(f)
        self._data = data
        return data

    def uptodate(self):
        raise NotImplementedError()
