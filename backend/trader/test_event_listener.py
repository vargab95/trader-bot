#!/usr/bin/python3

import unittest

from observer.event import SignalUpdatedEvent
from detector.common import TradingAction

from trader.event_listener import TradingActionListener


class TestTradingActionListener(unittest.TestCase):
    def setUp(self):
        self.listener = TradingActionListener()

    def test_single_hold_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.HOLD_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.HOLD_SIGNAL)

    def test_single_bullish_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BULLISH_SIGNAL)

    def test_single_bearish_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BEARISH_SIGNAL)

    def test_multiple_hold_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.HOLD_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.HOLD_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.HOLD_SIGNAL)

    def test_multiple_bullish_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BULLISH_SIGNAL)

    def test_multiple_bearish_signal(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BEARISH_SIGNAL)

    def test_hold_after_bull(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.HOLD_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BULLISH_SIGNAL)

    def test_hold_after_bear(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.HOLD_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BEARISH_SIGNAL)

    def test_bull_after_bear(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BULLISH_SIGNAL)

    def test_bear_after_bull(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BULLISH_SIGNAL))
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BEARISH_SIGNAL)

    def test_clear_on_read(self):
        self.listener.update(SignalUpdatedEvent("TestSignal", TradingAction.BEARISH_SIGNAL))
        self.assertEqual(self.listener.read_and_clear(), TradingAction.BEARISH_SIGNAL)
        self.assertEqual(self.listener.read_and_clear(), TradingAction.HOLD_SIGNAL)

    def test_invalid_signal(self):
        with self.assertRaises(ValueError):
            self.listener.update(SignalUpdatedEvent("TestSignal", 999))
