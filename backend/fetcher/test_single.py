#!/usr/bin/python3

import unittest
import unittest.mock

from config.trader import TraderConfig
from fetcher.single import TradingViewFetcherSingle
from fetcher.common import InvalidConfigurationException


@unittest.mock.patch("requests.post")
class SingleFetcherTest(unittest.TestCase):
    def test_empty_response(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

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

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherSingle(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(), 1.2)

    def test_invalid_market_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = ["market"]
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        try:
            TradingViewFetcherSingle(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass

    def test_invalid_candle_size_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = ["1m"]
        configuration.indicator = "all"

        try:
            TradingViewFetcherSingle(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass

    def test_invalid_indicator_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = ["all"]

        try:
            TradingViewFetcherSingle(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass

    def test_invalid_candle_size_value(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "invalid"
        configuration.indicator = "all"

        try:
            TradingViewFetcherSingle(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass

    def test_invalid_indicator_value(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "invalid"

        try:
            TradingViewFetcherSingle(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass
