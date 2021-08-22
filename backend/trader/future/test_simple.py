#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import config.detector
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.future.simple
import exchange.interface
from exchange.interface import Market
import exchange.factory
from detector.common import TradingAction

# TODO Test selling while in buying_bullish state
# TODO Test bullish signal comes when the trader is in buying_bearish state


class SimpleFutureTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({})
        cls.config.testing.enabled = True

        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-PERP"] = 100.0
        cls.exchange.price_mock["BEAR-PERP"] = 10.0
        cls.exchange.price_mock["BULL-PERP"] = 5.0
        cls.exchange.leverage = 3.0

    def setUp(self):
        self.trader = trader.future.simple.SimpleFutureTrader(TraderConfig({"market": "BTC-PERP"}), self.exchange)

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

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_startup_bullish(self):
        detector_signals = [
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

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

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

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

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_return_to_base_from_bullish(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_return_to_base_from_bearish(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_return_to_base_from_bullish_error(self):
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_return_to_base_from_bearish_error(self):
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

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

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_buy_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bearish", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bullish", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_sell_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_sell_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_buy_failure_when_switching_to_bearish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bearish", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_buy_failure_when_switching_to_bullish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bullish", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_sell_failure_when_switching_to_bearish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_sell_failure_when_switching_to_bullish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position", return_value=False):
            self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)


if __name__ == "__main__":
    unittest.main()
