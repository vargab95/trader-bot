#!/usr/bin/python3

import unittest
import datetime

from config.fetcher import FetcherConfig
from config.exchange import ExchangeConfig
from exchange.ftx_mock import FtxMock
import exchange.interface
import signals.trading_signal

from fetcher.exchange import ExchangeFetcher


class TestExchangeFetcher(unittest.TestCase):
    def test_fetched_value(self):
        exchange, fetcher = self.__generate_exchange_and_fetcher()

        exchange.price_mock["BSV-PERP"] = 10.0

        fetcher.fetch_technical_indicator()
        self.assertAlmostEqual(fetcher.get_technical_indicator(), 10.0)

    def test_get_historical_data(self):
        _, fetcher = self.__generate_exchange_and_fetcher()
        market = exchange.interface.Market("ETH", "BTC")
        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, datetime.datetime.now(), datetime.datetime.now(), 50, 1, datetime.timedelta(seconds=15))

        with unittest.mock.patch("time.sleep"):
            self.assertFalse(fetcher.get_indicator_history(descriptor))

    @staticmethod
    def __generate_exchange_and_fetcher():
        exchange = FtxMock(ExchangeConfig({
            "id": "ftx",
            "name": "ftx",
            "real_time": False
        }))
        return (exchange, ExchangeFetcher(
            FetcherConfig({
                "indicator_name": "BSV-PERP",
                "market": "BSV-PERP",
                "check_interval": 60
            }),
            exchange
        ))
