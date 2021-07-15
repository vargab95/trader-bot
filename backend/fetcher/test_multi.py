#!/usr/bin/python3

import unittest
import unittest.mock

from config.trader import TraderConfig
from fetcher.multi import TradingViewFetcherMulti
from fetcher.common import InvalidConfigurationException


# TODO Add assert to tests where that is missing
@unittest.mock.patch("requests.post")
class MultiFetcherTest(unittest.TestCase):
    def test_empty_response(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherMulti(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(), [])

    def test_fetch(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {
                    "s": "lll",
                    "d": [[1.2, 1.3, 1.4]]
                }
            ],
            "columns": ["all|1m"]
        }

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherMulti(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(),
                         {'lll': {'all': {'1m': [1.2, 1.3, 1.4]}}})

    def test_fetch_1d(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {
                    "s": "lll",
                    "d": [[1.2, 1.3, 1.4]]
                }
            ],
            "columns": ["all"]
        }

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1D"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherMulti(configuration)

        fetcher.fetch_technical_indicator()
        self.assertEqual(fetcher.get_technical_indicator(),
                         {'lll': {'all': {'1D': [1.2, 1.3, 1.4]}}})

    def test_invalid_market_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = ["market"]
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        TradingViewFetcherMulti(configuration)

    def test_invalid_candle_size_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = ["1m"]
        configuration.indicator = "all"

        TradingViewFetcherMulti(configuration)

    def test_invalid_indicator_type(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = ["all"]

        TradingViewFetcherMulti(configuration)

    def test_candle_and_indicator_list(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {
                    "s": "lll",
                    "d": [[1.2, 1.3, 1.4], [2.2, 2.3, 2.4]]
                }
            ],
            "columns": ["all|1m", "all|1h"]
        }

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = ["1m", "1h"]
        configuration.indicator = ["all"]

        fetcher = TradingViewFetcherMulti(configuration)
        fetcher.safe_fetch()
        self.assertEqual(
            fetcher.get_technical_indicator(),
            {
                'lll': {
                    'all': {
                        '1m': [1.2, 1.3, 1.4],
                        '1h': [2.2, 2.3, 2.4]
                    }
                }
            }
        )

    def test_invalid_candle_size_value(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "invalid"
        configuration.indicator = "all"

        try:
            TradingViewFetcherMulti(configuration)
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
            TradingViewFetcherMulti(configuration)
            self.fail()
        except InvalidConfigurationException:
            pass

    def test_safe_fetch(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {
                    "s": "lll",
                    "d": [[1.2, 1.3, 1.4]]
                }
            ],
            "columns": ["all|1m"]
        }

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherMulti(configuration)
        fetcher.safe_fetch()
        self.assertEqual(
            fetcher.get_technical_indicator(),
            {
                'lll': {
                    'all': {
                        '1m': [1.2, 1.3, 1.4]
                    }
                }
            }
        )

    def test_safe_fetch_fails(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.side_effect = Exception()
        post_mock.return_value.json.return_value = {}

        configuration = TraderConfig({})
        configuration.market = "market"
        configuration.candle_size = "1m"
        configuration.indicator = "all"

        fetcher = TradingViewFetcherMulti(configuration)
        fetcher.safe_fetch()
        self.assertEqual(fetcher.get_technical_indicator(), [])
