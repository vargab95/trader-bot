#!/usr/bin/python3

import unittest
import unittest.mock

from config.fetcher import FetcherConfig
from fetcher.single import TradingViewFetcherSingle
from fetcher.common import InvalidConfigurationException


@unittest.mock.patch("requests.post")
class SingleFetcherTest(unittest.TestCase):
    def test_empty_response(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "1m",
            "indicator": "all",
            "check_interval": 60
        })

        fetcher = TradingViewFetcherSingle(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(), None)

    def test_fetch(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {"d": [1.2]}
            ]
        }

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "1m",
            "indicator": "all",
            "check_interval": 60
        })

        fetcher = TradingViewFetcherSingle(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(), 1.2)

    def test_invalid_market_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": ["BTC-USD"],
            "candle_size": "1m",
            "indicator": "all",
            "check_interval": 60
        })

        with self.assertRaises(InvalidConfigurationException):
            TradingViewFetcherSingle(configuration)

    def test_invalid_candle_size_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": ["1m"],
            "indicator": "all",
            "check_interval": 60
        })

        with self.assertRaises(InvalidConfigurationException):
            TradingViewFetcherSingle(configuration)

    def test_invalid_indicator_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "1m",
            "indicator": ["all"],
            "check_interval": 60
        })

        with self.assertRaises(InvalidConfigurationException):
            TradingViewFetcherSingle(configuration)

    def test_invalid_candle_size_value(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "invalid",
            "indicator": "all",
            "check_interval": 60
        })

        with self.assertRaises(InvalidConfigurationException):
            TradingViewFetcherSingle(configuration)

    def test_invalid_indicator_value(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "1m",
            "indicator": "invalid",
            "check_interval": 60
        })

        with self.assertRaises(InvalidConfigurationException):
            TradingViewFetcherSingle(configuration)
