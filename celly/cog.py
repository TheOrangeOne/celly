import random

class Cog(object):
    def __init__(self, name=None, inputs={}, output=None):
        self.name = name
        self.inputs = inputs
        self.out = None
        if output:
            self.__call__ = output
        if not self.name:
            self.name = str(random.randint(0, 1000000))

    def __call__(self, **inputs):
        """
        Python by-passes the instance when __call__ is invoked and
        instead looks straight to the class.

        So we have to invoke the instance __call__ ourselves.
        """
        return self.__call__(**inputs)


class PrintCog(Cog):
    def __call__(self, **inputs):
        print(**inputs)
