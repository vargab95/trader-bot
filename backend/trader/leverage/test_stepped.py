#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import config.detector
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.leverage.stepped
import exchange.interface
import exchange.factory
from detector.common import TradingAction


class SteppedLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({})
        cls.config.testing.enabled = True
        cls.trader_config = TraderConfig({"max_steps": 10})

        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.leverage.stepped.SteppedLeverageTrader(self.trader_config, self.exchange)

    def tearDown(self):
        self.exchange.reset()

    def test_startup_hold(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_startup_bearish(self):
        detector_signals = [
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 1.0)

    def test_startup_bullish(self):
        detector_signals = [
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_hold(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_switches_to_bullish(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_switches_to_bearish(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 1.0)

    def test_exceeds_bullish(self):
        detector_signals = [TradingAction.BULLISH_SIGNAL for i in range(self.trader_config.max_steps + 1)]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_exceeds_bearish(self):
        detector_signals = [TradingAction.BEARISH_SIGNAL for i in range(self.trader_config.max_steps + 1)]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
