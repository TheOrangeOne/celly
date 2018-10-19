import json
import os

from celly.cog import Cog


class ReadJSONFileCog(Cog):
    def load_json(self, filename, directory):
        try:
            path = os.path.join(directory, filename)
            with open(path) as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return None

    def output(self, filename, directory):
        return self.load_json(filename, directory)


class WriteJSONFileCog(Cog):
    def store_json(self, filename, data, directory):
        path = os.path.join(directory, filename)
        with open(path, "w+") as f:
            json.dump(data, f)

    def output(self, filename, data, directory):
        return self.store_json(filename, data, directory)


class WriteFilesCog(Cog):
    def output(self, files, directory):
        for file in files:
            path = os.path.join(directory, file.name)
            if type(file.src) is bytes:
                mode = "wb+"
            else:
                mode = "w+"
            with open(path, mode) as f:
                f.write(file.src)


class FilterFilesDNECog(Cog):
    """
    Input: list of file names and a directory
    Output: list of files that don't exist
    """
    def output(self, files, directory):
        return list(filter(
            lambda f: not os.path.isfile(os.path.join(directory, f)),
            files
        ))
