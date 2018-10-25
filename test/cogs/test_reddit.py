import unittest
from unittest.mock import patch

from celly.cog import Cog
from celly.cogs.reddit import RedditUpdateSubsTopCog
from ..cog_utils import TestCase, TestCog


class TestRedditUpdateSubsTopCog(TestCase):
    def test_cached_one_team(self):
        self.wheel.add(Cog(
            name="current_date",
            output=lambda: "2018-10-22",
        ))
        self.wheel.add(Cog(
            name="cached_data",
            output=lambda: {
                "hockey": {
                    "2018-10-22": [
                        {
                            "title": "something something Gritty",
                        },
                    ],
                },
            }
        ))
        self.wheel.add(Cog(
            name="subreddits",
            output=lambda: [
                "hockey",
            ]
        ))
        self.wheel.add(RedditUpdateSubsTopCog(
            name="reddit_top",
            inputs=dict(
                cached_top="cached_data",
                date="current_date",
                subs="subreddits",
            )
        ))

        testcog = TestCog(
            inputs=dict(
                top="reddit_top",
            ),
            should_be_called_with=dict(
                top={
                    "hockey": {
                        "2018-10-22": [
                            {
                                "title": "something something Gritty",
                            },
                        ],
                    },
                }
            )
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    def test_cached_two_teams(self):
        self.wheel.add(Cog(
            name="current_date",
            output=lambda: "2018-10-22",
        ))
        self.wheel.add(Cog(
            name="cached_data",
            output=lambda: {
                "hockey": {
                    "2018-10-22": [
                        {
                            "title": "something something Gritty",
                        },
                    ],
                },
                "leafs": {
                    "2018-10-22": [
                        {
                            "title": "something Gritty",
                        },
                    ],
                },
            }
        ))
        self.wheel.add(Cog(
            name="subreddits",
            output=lambda: ["hockey", "leafs"]
        ))
        self.wheel.add(RedditUpdateSubsTopCog(
            name="reddit_top",
            inputs=dict(
                cached_top="cached_data",
                date="current_date",
                subs="subreddits",
            )
        ))

        testcog = TestCog(
            inputs=dict(
                top="reddit_top",
            ),
            should_be_called_with=dict(
                top={
                    "hockey": {
                        "2018-10-22": [
                            {
                                "title": "something something Gritty",
                            },
                        ],
                    },
                    "leafs": {
                        "2018-10-22": [
                            {
                                "title": "something Gritty",
                            },
                        ],
                    },
                }
            )
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    @patch('celly.web.get_reddit')
    def test_no_cache(self, mock_get_reddit):
        mock_get_reddit.side_effect = [
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "title": "hockey top",
                            },
                        },
                    ]
                }
            },
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "title": "leafs top",
                            },
                        },
                    ]
                }
            }
        ]

        self.wheel.add(Cog(
            name="current_date",
            output=lambda: "2018-10-22",
        ))
        self.wheel.add(Cog(
            name="cached_data",
            output=lambda: None
        ))
        self.wheel.add(Cog(
            name="subreddits",
            output=lambda: ["hockey", "leafs"]
        ))
        self.wheel.add(RedditUpdateSubsTopCog(
            name="reddit_top",
            inputs=dict(
                cached_top="cached_data",
                date="current_date",
                subs="subreddits",
            )
        ))

        testcog = TestCog(
            inputs=dict(
                top="reddit_top",
            ),
            should_be_called_with=dict(
                top={
                    "hockey": {
                        "2018-10-22": [
                            {
                                "title": "hockey top"
                            }
                        ]
                    },
                    "leafs": {
                        "2018-10-22": [
                            {
                                "title": "leafs top"
                            }
                        ]
                    }
                }
            )
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    @patch('celly.web.get_reddit')
    def test_partial_cache(self, mock_get_reddit):
        mock_get_reddit.side_effect = [
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "title": "leafs top",
                            },
                        },
                    ]
                }
            },
        ]

        self.wheel.add(Cog(
            name="current_date",
            output=lambda: "2018-10-22",
        ))
        self.wheel.add(Cog(
            name="cached_data",
            output=lambda: {
                "hockey": {
                    "2018-10-22": [
                        {
                            "title": "hockey top",
                        },
                    ],
                },
                "leafs": {
                },
            }
        ))
        self.wheel.add(Cog(
            name="subreddits",
            output=lambda: ["hockey", "leafs"]
        ))
        self.wheel.add(RedditUpdateSubsTopCog(
            name="reddit_top",
            inputs=dict(
                cached_top="cached_data",
                date="current_date",
                subs="subreddits",
            )
        ))

        testcog = TestCog(
            inputs=dict(
                top="reddit_top",
            ),
            should_be_called_with=dict(
                top={
                    "hockey": {
                        "2018-10-22": [
                            {
                                "title": "hockey top"
                            }
                        ]
                    },
                    "leafs": {
                        "2018-10-22": [
                            {
                                "title": "leafs top"
                            }
                        ]
                    }
                }
            )
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()

    @patch('celly.web.get_reddit')
    def test_prev_day_cache(self, mock_get_reddit):
        mock_get_reddit.side_effect = [
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "title": "hockey top 23",
                            },
                        },
                    ]
                }
            },
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "title": "leafs top 23",
                            },
                        },
                    ]
                }
            },
        ]

        self.wheel.add(Cog(
            name="current_date",
            output=lambda: "2018-10-23",
        ))
        self.wheel.add(Cog(
            name="cached_data",
            output=lambda: {
                "hockey": {
                    "2018-10-22": [
                        {
                            "title": "hockey top 1"
                        },
                        {
                            "title": "hockey top 2"
                        }
                    ],
                },
                "leafs": {
                },
            }
        ))
        self.wheel.add(Cog(
            name="subreddits",
            output=lambda: ["hockey", "leafs"]
        ))
        self.wheel.add(RedditUpdateSubsTopCog(
            name="reddit_top",
            inputs=dict(
                cached_top="cached_data",
                date="current_date",
                subs="subreddits",
            )
        ))

        testcog = TestCog(
            inputs=dict(
                top="reddit_top",
            ),
            should_be_called_with=dict(
                top={
                    "hockey": {
                        "2018-10-22": [
                            {
                                "title": "hockey top 1"
                            },
                            {
                                "title": "hockey top 2"
                            }
                        ],
                        "2018-10-23": [
                            {
                                "title": "hockey top 23"
                            }
                        ]
                    },
                    "leafs": {
                        "2018-10-23": [
                            {
                                "title": "leafs top 23"
                            }
                        ]
                    }
                }
            )
        )

        self.wheel.add(testcog)
        self.wheel.start()
        testcog.test()
