#!/usr/bin/python3

import unittest
import unittest.mock

from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.single.simple
import exchange.interface
import exchange.factory
from detector.common import TradingAction
from trader.common import TraderState


class SimpleSingleTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: TraderConfig = TraderConfig({"market": "BTC-USDT"})
        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-USDT"] = 100.0

    def setUp(self):
        self.trader = trader.single.simple.SimpleSingleMarketTrader(self.config, self.exchange)

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

    def test_return_to_base(self):
        detector_signals = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)

    def test_sell_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 1.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BTC"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_auto_detect_start_state_in_bullish(self):
        self.exchange.set_balance(self.config.market.target, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BULLISH)

    def test_auto_detect_start_state_only_for_the_first_time(self):
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.exchange.set_balance(self.config.market.target, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)

    def test_auto_detect_start_state_in_base(self):
        self.exchange.set_balance(self.config.market.target, 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)


if __name__ == "__main__":
    unittest.main()
