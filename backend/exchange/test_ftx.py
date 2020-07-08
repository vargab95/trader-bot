#!/usr/bin/python3

import datetime
import unittest
import unittest.mock

import config.application
import exchange.factory
import exchange.interface
import signals.trading_signal


@unittest.mock.patch("requests.get")
@unittest.mock.patch("requests.Session.send")
class BinanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = False
        cls.config.exchange.name = "ftx"
        cls.config.exchange.market_name_format = "{target}/{base}"
        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format

    def init_controller(self, _, get_mock, min_size, min_notional):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "name": "BTC/ETH",
                    "minProvideSize": min_size,
                    "priceIncrement": min_notional
                }
            ]
        }

        return exchange.factory.ExchangeControllerFactory.create(
            self.config)

    def test_init_failure(self, _, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }

        try:
            exchange.factory.ExchangeControllerFactory.create(
                self.config)
            self.fail()
        except exchange.interface.ExchangeError:
            pass

    def test_get_price(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        market = exchange.interface.Market("ETH", "BTC")
        self.assertAlmostEqual(controller.get_price(market), 1.2)

    def test_get_price_failure(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }

        market = exchange.interface.Market("ETH", "BTC")

        with unittest.mock.patch("time.sleep"):
            controller.get_price(market)

    def test_get_balance(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        market = exchange.interface.Market("ETH", "BTC")
        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "free": 1.2,
                    "coin": market.target
                }
            ]
        }

        self.assertAlmostEqual(controller.get_balance(market.target), 1.2)

    def test_get_non_existing_balance(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        market = exchange.interface.Market("BNB", "BTC")
        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "free": 1.2,
                    "coin": "BTC/ETH"
                }
            ]
        }

        self.assertAlmostEqual(controller.get_balance(market), 0.0)

    def test_buy(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")

        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": "Success"
        }
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        self.assertTrue(controller.buy(market, 2.0))

    def test_buy_failure(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")

        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        with unittest.mock.patch("time.sleep"):
            self.assertFalse(controller.buy(market, 2.0))

    def test_buy_negative(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        self.assertFalse(controller.buy(market, -2.0))

    def test_buy_below_notional(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        self.assertFalse(controller.buy(market, 0.1))

    def test_sell(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")

        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": "Success"
        }
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        self.assertTrue(controller.sell(market, 2.0))

    def test_sell_failure(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")

        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        with unittest.mock.patch("time.sleep"):
            self.assertFalse(controller.sell(market, 2.0))

    def test_sell_negative(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        self.assertFalse(controller.sell(market, -2.0))

    def test_sell_below_notional(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        self.assertFalse(controller.sell(market, 0.1))

    def test_historical_price(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("USD", "BTC")

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

        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, None, None, 50, 1, datetime.timedelta(seconds=15))
        self.assertListEqual(
            [signals.trading_signal.TradingSignalPoint(
                value=11055.25, date=datetime.datetime(2019, 6, 24, 17, 15))],
            controller.get_price_history(
                descriptor, keyword="close").data
        )
