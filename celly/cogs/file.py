import json

from celly.cog import Cog


class ReadJSONFileCog(Cog):
    def load_json(self, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return None

    def output(self, filename):
        return self.load_json(filename)


class WriteJSONFileCog(Cog):
    def store_json(self, filename, data):
        with open(filename, 'w+') as f:
            json.dump(data, f)

    def output(self, filename, data):
        return self.store_json(filename, data)
