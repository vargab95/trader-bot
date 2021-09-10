#!/usr/bin/python3

import datetime
import unittest
import unittest.mock

from config.exchange import ExchangeConfig
import exchange.factory
import exchange.interface
import signals.trading_signal


@unittest.mock.patch("requests.get")
@unittest.mock.patch("requests.Session.send")
class FtxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: ExchangeConfig = ExchangeConfig({})
        cls.config.name = "ftx"
        cls.config.market_name_format = "{target}/{base}"
        cls.config.private_key = "test_prv_key"
        cls.config.public_key = "test_pub_key"

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

        return exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)

    def test_init_failure(self, _, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }

        with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
            exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)

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

    def test_get_price_with_future(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "ask": 1.3,
                "bid": 1.4
            }
        }

        market = exchange.interface.Market("BSV", "PERP")
        self.assertAlmostEqual(controller.get_price(market, future=True), 1.3)

    def test_get_price_with_future_and_keyword(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "ask": 1.3,
                "bid": 1.4
            }
        }

        market = exchange.interface.Market("BSV", "PERP")
        self.assertAlmostEqual(controller.get_price(market, keyword="bid", future=True), 1.4)

    def test_get_price_failure(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": False,
            "error": "Connection error"
        }

        market = exchange.interface.Market("ETH", "BTC")

        with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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

    def test_get_position(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        market = exchange.interface.Market("PERP", "BSV")
        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "netSize": 1.2,
                    "future": "BSV/PERP"
                }
            ]
        }

        self.assertAlmostEqual(controller.get_position(market), 1.2)

    def test_get_non_existing_position(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        market = exchange.interface.Market("BSV", "PERP")
        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "netSize": 1.2,
                    "future": "BTC-PERP"
                }
            ]
        }

        self.assertAlmostEqual(controller.get_position(market), 0.0)

    def test_bet_on_bearish(self, session_mock, get_mock):
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

        controller.bet_on_bearish(market, 2.0)

    def test_bet_on_bullish(self, session_mock, get_mock):
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

        controller.bet_on_bullish(market, 2.0)

    def test_get_leverage_balance(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)

        session_mock.return_value = unittest.mock.Mock()
        session_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "totalAccountValue": 2.0,
                "leverage": 3.0,
                "totalPositionSize": 1.5
            }
        }

        self.assertAlmostEqual(controller.get_leverage_balance(), 4.5)

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

        controller.buy(market, 2.0)

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

        with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
            controller.buy(market, 2.0)

    def test_buy_negative(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, -2.0)

    def test_buy_below_notional(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, 0.1)

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

        controller.sell(market, 2.0)

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

        with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
            controller.sell(market, 2.0)

    def test_sell_negative(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.sell(market, -2.0)

    def test_sell_below_notional(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("ETH", "BTC")
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.sell(market, 0.1)

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
            market, datetime.datetime.now(), datetime.datetime.now(), 50, 1, datetime.timedelta(seconds=15))
        self.assertListEqual(
            [signals.trading_signal.TradingSignalPoint(
                value=11055.25, date=datetime.datetime(2019, 6, 24, 17, 15))],
            controller.get_price_history(descriptor).data)

    def test_historical_price_invalid_resolution(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("USD", "BTC")
        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, None, None, 50, 1, datetime.timedelta(seconds=25))

        with self.assertRaises(ValueError):
            self.assertFalse(controller.get_price_history(descriptor))

    def test_historical_price_failure(self, session_mock, get_mock):
        controller = self.init_controller(session_mock, get_mock, 1.0, 1.0)
        market = exchange.interface.Market("USD", "BTC")

        get_mock.return_value.json.return_value = {
            "success": False,
            "error": ""
        }

        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, datetime.datetime.now(), datetime.datetime.now(), 50, 1, datetime.timedelta(seconds=15))
        with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
            controller.get_price_history(descriptor)
