import unittest

from celly.cog import Cog


class TestCog(unittest.TestCase):
    def test_cog(self):
        cog = Cog(
            "test",
            inputs=["1", "2", "3"]
        )

    def test_lambda_cog(self):
        cog = Cog(
            "test",
            output=lambda: "test_data"
        )
        assert cog.output() == "test_data"
