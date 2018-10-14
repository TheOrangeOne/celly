import random

class Cog(object):
    def __init__(self, name=None, inputs=[], output=None):
        self.name = name
        self.inputs = inputs
        self.out = None
        if output:
            self.output = output
        if not self.name:
            self.name = str(random.randint(0, 10000))

    def output(*inputs):
        raise NotImplementedError()

class PrintCog(Cog):
    def output(self, *inputs):
        print(*inputs)
