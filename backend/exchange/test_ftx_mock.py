#!/usr/bin/python3

import unittest.mock

from datetime import datetime, timedelta

from signals.trading_signal import TickerSignalDescriptor, TradingSignalPoint
from config.exchange import ExchangeConfig

import exchange.factory
import exchange.interface
from exchange.interface import Market

import exchange.test_mock_common


class FtxMockTest(exchange.test_mock_common.CommonMockTest):
    @classmethod
    def setUpClass(cls):
        cls.config: ExchangeConfig = ExchangeConfig({})
        cls.config.real_time = False
        cls.config.start_money = 100.0
        cls.config.fee = 0.0
        cls.config.name = "ftx"
        cls.config.market_name_format = "{target}-{base}"
        cls.controller = exchange.factory.ExchangeControllerFactory.create(cls.config, testing=True)

    @unittest.mock.patch("requests.get")
    @unittest.mock.patch("requests.Session.send")
    def test_get_price_unsuccessful(self, _, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertFalse(self.controller.get_price(exchange.interface.Market.create_from_string("BEAR-USDT")))
        self.controller.set_real_time(False)

    @unittest.mock.patch("requests.get")
    @unittest.mock.patch("requests.Session.send")
    def test_get_price_successful(self, _, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "name": "BEAR/USDT",
                    "minProvideSize": 0.0,
                    "priceIncrement": 0.0,
                }
            ]
        }

        self.controller.set_real_time(True)

        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }
        with unittest.mock.patch("time.sleep"):
            self.assertAlmostEqual(self.controller.get_price(Market.create_from_string("BEAR-USDT")), 1.2)
        self.controller.set_real_time(False)

    @unittest.mock.patch("requests.get")
    @unittest.mock.patch("requests.Session.send")
    def test_historical_price(self, _, get_mock):
        market = exchange.interface.Market("USD", "BTC")

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "name": "BEAR/USDT",
                    "minProvideSize": 0.0,
                    "priceIncrement": 0.0,
                }
            ]
        }

        self.controller.set_real_time(True)

        get_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "close": 11055.25,
                    "high": 11089.0,
                    "low": 11043.5,
                    "open": 11059.25,
                    "startTime": "2019-06-24T17:15:00+00:00",
                    "volume": 464193.95725
                }
            ]
        }

        descriptor = TickerSignalDescriptor(market, datetime.now(), datetime.now(), 50, 1, timedelta(seconds=15))
        with unittest.mock.patch("time.sleep"):
            self.assertListEqual(
                [TradingSignalPoint(value=11055.25, date=datetime(2019, 6, 24, 17, 15))],
                self.controller.get_price_history(descriptor, keyword="close").data)

        self.controller.set_real_time(False)


if __name__ == "__main__":
    unittest.main()
