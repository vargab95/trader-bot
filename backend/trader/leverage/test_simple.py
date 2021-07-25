#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import config.detector
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.leverage.simple
import exchange.interface
import exchange.factory
from detector.common import TradingAction

# TODO Test selling while in buying_bullish state
# TODO Test bullish signal comes when the trader is in buying_bearish state


class SimpleLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({})
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"

        exchange.interface.Market.name_format = cls.config.exchange.market_name_format
        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.leverage.simple.SimpleLeverageTrader(TraderConfig({}), self.exchange)

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

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_startup_bullish(self):
        detector_signals = [
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_hold(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bullish(self):
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

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bearish(self):
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

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_buy_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_sell_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)

    def test_sell_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
