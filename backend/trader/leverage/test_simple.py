#!/usr/bin/python3

import unittest
import unittest.mock

import config.detector
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.leverage.simple
import exchange.interface
import exchange.factory
from detector.common import TradingAction
from trader.common import TraderState

# TODO Test selling while in buying_bullish state
# TODO Test bullish signal comes when the trader is in buying_bearish state


class SimpleLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: TraderConfig = TraderConfig({})

        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.leverage.simple.SimpleLeverageTrader(self.config, self.exchange)

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

    def test_buy_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_sell_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)

    def test_sell_failure_when_returning_to_base_from_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_sell_failure_when_returning_to_base_from_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_auto_detect_start_state_in_bull(self):
        self.exchange.set_balance(self.config.bullish_market.target, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BULLISH)

    def test_auto_detect_start_state_in_bear(self):
        self.exchange.set_balance(self.config.bearish_market.target, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BEARISH)

    def test_auto_detect_start_state_only_for_the_first_time(self):
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.exchange.set_balance(self.config.bearish_market.target, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)

    def test_auto_detect_start_state_in_base(self):
        self.exchange.set_balance(self.config.bearish_market.target, 0.0)
        self.exchange.set_balance(self.config.bullish_market.target, 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)


if __name__ == "__main__":
    unittest.main()
