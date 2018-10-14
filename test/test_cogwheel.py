import unittest
import unittest.mock as mock

from celly.cog import Cog
from celly.cogwheel import CogWheel

from test.cog_utils import TestCog


class TestCogWheel(unittest.TestCase):
    def setUp(self):
        self.engine = CogWheel()
        pass

    def test_basic(self):
        class DataCog(Cog):
            def output(self):
                return "test"
        cog = TestCog("2", inputs=["1"])
        cog.output = mock.Mock()

        self.engine.add(DataCog("1", inputs=[]))
        self.engine.add(cog)
        self.engine.start()

        cog.output.assert_called_once()
        cog.output.assert_called_with("test")


    def test_multiple_inputs(self):
        class DataCog1(Cog):
            def output(self):
                return "test1"
        class DataCog2(Cog):
            def output(self):
                return "test2"
        class DataCog3(Cog):
            def output(self):
                return "test3"

        cog = TestCog("testCog", inputs=["1", "2", "3"])
        cog.output = mock.Mock()

        self.engine.add(DataCog1("1", inputs=[]))
        self.engine.add(DataCog2("2", inputs=[]))
        self.engine.add(DataCog3("3", inputs=[]))
        self.engine.add(cog)
        self.engine.start()

        cog.output.assert_called_once()
        cog.output.assert_called_with("test1", "test2", "test3")

    def test_multiple_read_cogs(self):
        class DataCog1(Cog):
            def output(self):
                return "test1"
        class DataCog2(Cog):
            def output(self):
                return "test2"
        class DataCog3(Cog):
            def output(self):
                return "test3"

        cog1 = TestCog("test1", inputs=["1", "2", "3"])
        cog1.output = mock.Mock()

        cog2 = TestCog("test2", inputs=["1", "2"])
        cog2.output = mock.Mock()

        self.engine.add(DataCog1("1", inputs=[]))
        self.engine.add(DataCog2("2", inputs=[]))
        self.engine.add(DataCog3("3", inputs=[]))
        self.engine.add(cog1)
        self.engine.add(cog2)
        self.engine.start()

        cog1.output.assert_called_once()
        cog1.output.assert_called_with("test1", "test2", "test3")
        cog2.output.assert_called_once()
        cog2.output.assert_called_with("test1", "test2")

    def test_long_cog_chain(self):
        class Cog1(Cog):
            def output(self):
                return "1"
        class Cog2(Cog):
            def output(self, data):
                return data + "2"
        class Cog3(Cog):
            def output(self, data):
                return data + "3"

        cog = TestCog("test", inputs=["3"])
        cog.output = mock.Mock()

        self.engine.add(Cog1("1", inputs=[]))
        self.engine.add(Cog2("2", inputs=["1"]))
        self.engine.add(Cog3("3", inputs=["2"]))
        self.engine.add(cog)
        self.engine.start()

        cog.output.assert_called_once()
        cog.output.assert_called_with("123")
