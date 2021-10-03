import unittest

from config.common import InvalidConfigurationException
from config.fetcher import FetcherConfig


class TestFetcherConfig(unittest.TestCase):
    def setUp(self):
        self.conf = FetcherConfig({})

    def test(self):
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()
