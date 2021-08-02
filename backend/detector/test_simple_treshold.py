#!/usr/bin/python3

import unittest

from detector.simple_treshold import SimpleTresholdDetector
from detector.common import TradingAction


class TestSimpleTresholdDetector(unittest.TestCase):
    def do_test(self, indicators, expected_results, bullish_threshold=0.4, bearish_threshold=-0.4):
        self.assertEqual(len(indicators), len(expected_results))

        detector = SimpleTresholdDetector(bearish_threshold, bullish_threshold)

        for indicator, expected_result in zip(indicators, expected_results):
            self.assertEqual(expected_result, detector.check(indicator))

    def test_between_bullish_and_bearish(self):
        self.do_test([-0.2, -0.1, 0.0, 0.1, 0.2], [TradingAction.HOLD_SIGNAL for _ in range(5)])

    def test_over_bullish(self):
        self.do_test([1.2, 1.1, 1.0, 1.1, 1.2], [TradingAction.BULLISH_SIGNAL for _ in range(5)])

    def test_below_bearish(self):
        self.do_test([-1.2, -1.1, -1.0, -1.1, -1.2], [TradingAction.BEARISH_SIGNAL for _ in range(5)])

    def test_pass_bullish(self):
        self.do_test([0.2, 0.1, 0.0, 0.5, 0.6], [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.BULLISH_SIGNAL
        ])

    def test_pass_bearish(self):
        self.do_test([0.2, 0.1, 0.0, -0.5, -0.6], [
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL
        ])

    def test_switch_back_from_bearish(self):
        self.do_test([-0.5, -0.45, 0.0, 0.1, 0.2], [
            TradingAction.BEARISH_SIGNAL,
            TradingAction.BEARISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ])

    def test_switch_back_from_bullish(self):
        self.do_test([0.5, 0.45, 0.0, 0.1, 0.2], [
            TradingAction.BULLISH_SIGNAL,
            TradingAction.BULLISH_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL,
            TradingAction.HOLD_SIGNAL
        ])
