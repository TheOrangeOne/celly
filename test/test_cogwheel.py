import unittest

from celly.cog import Cog
from celly.cogwheel import (
    CogWheel,
    CogArgError,
    CogMissingError,
)
from .cog_utils import TestCog


class TestCogWheel(unittest.TestCase):
    def setUp(self):
        self.engine = CogWheel()

    def test_no_work(self):
        self.engine.start()

    def test_cog(self):
        class MyCog(Cog):
            def __call__(self):
                return "testvalue"
        self.engine.add(MyCog(
            name="1",
        ))
        testcog = TestCog(
            name="2",
            inputs=dict(
                test="1",
            ),
            should_be_called_with=dict(
                test="testvalue"
            ),
        )
        self.engine.add(testcog)
        self.engine.start()
        testcog.test()

    def test_lambda_cog(self):
        self.engine.add(Cog(
            name="1",
            output=lambda: "testvalue",
        ))
        testcog = TestCog(
            name="2",
            inputs=dict(
                test="1",
            ),
            should_be_called_with=dict(
                test="testvalue"
            ),
        )
        self.engine.add(testcog)
        self.engine.start()
        testcog.test()

    def test_multiple_inputs(self):
        self.engine.add(Cog(
            name="1",
            output=lambda: "test1",
        ))
        self.engine.add(Cog(
            name="2",
            output=lambda: "test2",
        ))
        self.engine.add(Cog(
            name="3",
            output=lambda: "test3",
        ))
        testcog = TestCog(
            inputs=dict(
                input1="1",
                input2="2",
                input3="3",
            ),
            should_be_called_with=dict(
                input1="test1",
                input2="test2",
                input3="test3",
            )
        )
        self.engine.add(testcog)
        self.engine.start()
        testcog.test()

    def test_missing_initial_deps(self):
        self.engine.add(Cog(
            inputs=dict(
                input1="ineedthisinput"
            )
        ))
        with self.assertRaises(CogMissingError):
            self.engine.start()

    def test_missing_deps(self):
        """
        Test that an appropriate assertion is raised when a cog
        declares an input that is not provided.
        """
        self.engine.add(Cog(
            output=lambda: "out"
        ))
        self.engine.add(Cog(
            inputs=dict(
                input1="ineedthisinput"
            )
        ))
        with self.assertRaises(CogMissingError):
            self.engine.start()

    def test_missing_args(self):
        self.engine.add(Cog(
            name="input1",
            output=lambda: "out"
        ))
        self.engine.add(Cog(
            name="input2",
            output=lambda: "out"
        ))

        class MyCog(Cog):
            def __call__(self, input1=None):
                pass

        self.engine.add(MyCog(
            inputs=dict(
                input1="input1",
                input2="input2",
            )
        ))
        with self.assertRaises(CogArgError):
            self.engine.start()

    def test_multiple_read_cogs(self):
        class DataCog1(Cog):
            def __call__(self):
                return "test1"
        class DataCog2(Cog):
            def __call__(self):
                return "test2"
        class DataCog3(Cog):
            def __call__(self):
                return "test3"

        testcog1 = TestCog(
            inputs=dict(
                arg1="1",
                arg2="2",
                arg3="3",
            ),
            should_be_called_with=dict(
                arg1="test1",
                arg2="test2",
                arg3="test3",
            ),
        )
        testcog2 = TestCog(
            inputs=dict(
                arg1="1",
                arg2="2",
            ),
            should_be_called_with=dict(
                arg1="test1",
                arg2="test2",
            ),
        )

        self.engine.add(DataCog1("1"))
        self.engine.add(DataCog2("2"))
        self.engine.add(DataCog3("3"))
        self.engine.add(testcog1)
        self.engine.add(testcog2)
        self.engine.start()

        testcog1.test()
        testcog2.test()

    def test_long_cog_chain(self):
        self.engine.add(Cog(
            name="1",
            output=lambda: "1"
        ))
        self.engine.add(Cog(
            name="2",
            inputs=dict(
                d="1",
            ),
            output=lambda d: d + "2",
        ))
        self.engine.add(Cog(
            name="3",
            inputs=dict(
                d="2"
            ),
            output=lambda d: d + "3",
        ))
        testcog = TestCog(
            inputs=dict(
                d="3"
            ),
            should_be_called_with=dict(
                d="123",
            )
        )
        self.engine.add(testcog)
        self.engine.start()

        testcog.test()
