#!/usr/bin/python3

import unittest
import unittest.mock

from config.trader import TraderConfig
from config.exchange import ExchangeConfig
import trader.future.simple
import exchange.interface
from exchange.interface import Market
import exchange.factory
from detector.common import TradingAction
from trader.common import TraderState

# TODO Test selling while in buying_bullish state
# TODO Test bullish signal comes when the trader is in buying_bearish state


class SimpleFutureTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: TraderConfig = TraderConfig({"market": "BTC-PERP"})

        exchange_config = ExchangeConfig({"name": "ftx", "real_time": False})
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(exchange_config, testing=True)

    def setUp(self):
        self.trader = trader.future.simple.SimpleFutureTrader(self.config, self.exchange)
        self.exchange.price_mock["BTC-PERP"] = 100.0
        self.exchange.price_mock["BEAR-PERP"] = 10.0
        self.exchange.price_mock["BULL-PERP"] = 5.0
        self.exchange.leverage = 3.0

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

    def test_multiple_bearish_with_returning_without_price_change(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal in detector_signals:
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_bearish_with_returning(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BEARISH_SIGNAL, 100.0),
            (TradingAction.BEARISH_SIGNAL, 75.0),
            (TradingAction.BEARISH_SIGNAL, 50.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 50.0)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 400.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_bullish_with_returning(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 150.0),
            (TradingAction.BULLISH_SIGNAL, 200.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 200.0)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 400.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_from_bullish_to_bearish_with_changing_money_to_zero(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 150.0),
            (TradingAction.BULLISH_SIGNAL, 200.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 250.0),
            (TradingAction.BEARISH_SIGNAL, 300.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 300.0)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_from_bullish_to_bearish_with_changing_money_to_higher_money(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 150.0),
            (TradingAction.BULLISH_SIGNAL, 200.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 150.0),
            (TradingAction.BEARISH_SIGNAL, 100.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 100.0)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 1600.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_from_bearish_to_bullish_with_changing_money_to_zero(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 150.0),
            (TradingAction.BEARISH_SIGNAL, 100.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 75.0),
            (TradingAction.BULLISH_SIGNAL, 66.66667),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 66.66667)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0, 2)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_from_bearish_to_bullish_with_changing_money_to_higher_money(self):
        detector_signals = [
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.HOLD_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 200.0),
            (TradingAction.BEARISH_SIGNAL, 150.0),
            (TradingAction.BEARISH_SIGNAL, 100.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.HOLD_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 100.0),
            (TradingAction.BULLISH_SIGNAL, 150.0),
            (TradingAction.BULLISH_SIGNAL, 200.0),
            (TradingAction.RETURN_TO_BASE_SIGNAL, 200.0)
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for detector_signal, price in detector_signals:
            self.exchange.price_mock["BTC-PERP"] = price
            self.trader.perform(detector_signal)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 1600.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)

    def test_multiple_bullish_with_returning_without_price_change(self):
        detector_signals = [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.RETURN_TO_BASE_SIGNAL
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bearish",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bullish",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_buy_failure_when_switching_to_bearish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bearish",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BEARISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)

    def test_buy_failure_when_switching_to_bullish_without_resignal(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(TradingAction.HOLD_SIGNAL)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.bet_on_bullish",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
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
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.close_position",
                                 side_effect=exchange.interface.UnknownProviderExchangeError):
            with self.assertRaises(exchange.interface.UnknownProviderExchangeError):
                self.trader.perform(TradingAction.BULLISH_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), -3.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 0.0)
        self.assertAlmostEqual(self.exchange.get_position(Market("PERP", "BTC")), 3.0)

    def test_auto_detect_start_state_in_bull(self):
        self.exchange.set_position(self.config.market, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BULLISH)

    def test_auto_detect_start_state_in_bear(self):
        self.exchange.set_position(self.config.market, -1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BEARISH)

    def test_auto_detect_start_state_only_for_the_first_time(self):
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.exchange.set_position(self.config.market, 1.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)

    def test_auto_detect_start_state_in_base(self):
        self.exchange.set_position(self.config.market, 0.0)
        self.trader.perform(TradingAction.HOLD_SIGNAL)
        self.assertEqual(self.trader.state, TraderState.BASE)


if __name__ == "__main__":
    unittest.main()
