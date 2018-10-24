import unittest

from celly.cog import Cog


class TestCog(unittest.TestCase):
    def test_cog(self):
        cog = Cog(
            name="test",
            inputs=dict(
                arg1="1",
                arg2="2",
                arg3="3",
            ),
        )

    def test_lambda_cog(self):
        cog = Cog(
            "test",
            output=lambda: "test_data"
        )
        assert cog() == "test_data"
