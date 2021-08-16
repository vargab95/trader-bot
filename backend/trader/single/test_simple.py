#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.single.simple
import exchange.interface
import exchange.factory
from detector.common import TradingAction


class SimpleSingleTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({})
        cls.config.testing.enabled = True

        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.single.simple.SimpleSingleMarketTrader(TraderConfig({}), self.exchange)

    def tearDown(self):
        self.exchange.reset()

    def test_startup_between(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_startup_bearish(self):
        detector_signals = [
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_startup_bullish(self):
        detector_signals = [
            TradingAction.BULLISH_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.BULLISH_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)

    def test_hold(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_switch_to_bullish(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.BULLISH_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)

    def test_switch_to_bearish(self):
        detector_signals = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)

    def test_sell_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)


if __name__ == "__main__":
    unittest.main()
