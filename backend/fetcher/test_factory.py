#!/usr/bin/python3

import unittest

from config.fetcher import FetcherConfig
from fetcher.factory import FetcherFactory, InvalidFetcherFactoryParameter
from fetcher.single import TradingViewFetcherSingle
from fetcher.multi import TradingViewFetcherMulti
from fetcher.exchange import ExchangeFetcher


class TestFetcherFactory(unittest.TestCase):
    def test_create_trading_view_fetcher_single(self):
        config = FetcherConfig({
            "type": "trading_view",
            "candle_size": "1h",
            "market": "BTC-USD",
            "check_interval": 60
        })

        self.assertIsInstance(FetcherFactory.create(config), TradingViewFetcherSingle)

    def test_create_trading_view_fetcher_multi(self):
        config = FetcherConfig({
            "type": "trading_view",
            "candle_size": ["1m", "5m"],
            "market": "BTC-USD",
            "check_interval": 60
        })

        self.assertIsInstance(FetcherFactory.create(config), TradingViewFetcherMulti)

    def test_create_exchange_fetcher(self):
        config = FetcherConfig({
            "type": "exchange",
            "candle_size": "1m",
            "market": "BTC-USD",
            "check_interval": 60
        })

        self.assertIsInstance(FetcherFactory.create(config), ExchangeFetcher)

    def test_create_invalid(self):
        config = FetcherConfig({
            "type": "invalid",
            "candle_size": "1m",
            "market": "BTC-USD",
            "check_interval": 60
        })

        with self.assertRaises(InvalidFetcherFactoryParameter):
            FetcherFactory.create(config)


if __name__ == "__main__":
    unittest.main()
