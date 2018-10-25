import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogwheel import CogWheel


class TestCog(Cog):
    def __init__(self, *args, **kwargs):
        self.expected = kwargs.pop('should_be_called_with', None)
        super().__init__(*args, **kwargs)
        self.__call__ = mock.Mock()

    def test(self):
        self.__call__.assert_called_once()
        if self.expected:
            self.__call__.assert_called_with(**self.expected)


class TestCase(unittest.TestCase):
    def setUp(self):
        self.wheel = CogWheel()
