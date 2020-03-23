#!/usr/bin/python3

import unittest

import detector.reverse_rising_edge
import actions


class ReverseRisingEdgeDetectorTest(unittest.TestCase):
    def test_quick_fall_down(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.0, 0.0)
        test_data = [[-0.066667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.066668, actions.TradingAction.HOLD],
                     [-0.021212, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [-0.378788, actions.TradingAction.HOLD],
                     [-0.378789, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_slow_up_trend(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.0, 0.0)
        test_data = [[-0.045455, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.045456, actions.TradingAction.HOLD],
                     [-0.045457, actions.TradingAction.HOLD],
                     [0.066667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [0.0, actions.TradingAction.HOLD],
                     [0.01, actions.TradingAction.HOLD],
                     [0.02, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_trend_with_same_but_modified_threshold(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.1, 0.1)
        test_data = [[-0.145455, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.145456, actions.TradingAction.HOLD],
                     [-0.145457, actions.TradingAction.HOLD],
                     [0.166667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [0.1, actions.TradingAction.HOLD],
                     [0.11, actions.TradingAction.HOLD],
                     [0.12, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_with_same_but_modified_threshold(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            -0.1, -0.1)
        test_data = [[-0.166667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.166668, actions.TradingAction.HOLD],
                     [-0.121212, actions.TradingAction.HOLD],
                     [-0.1, actions.TradingAction.HOLD],
                     [-0.11, actions.TradingAction.HOLD],
                     [-0.478788, actions.TradingAction.HOLD],
                     [-0.478789, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_trend_with_different_and_modified_threshold(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.1, -0.1)
        test_data = [[-0.15, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.1, actions.TradingAction.HOLD],
                     [-0.05, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [0.05, actions.TradingAction.HOLD],
                     [0.1, actions.TradingAction.HOLD],
                     [0.166667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [0.1, actions.TradingAction.HOLD],
                     [0.11, actions.TradingAction.HOLD],
                     [0.12, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_with_different_and_modified_threshold(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.33, -0.33)
        test_data = [[-0.166667, actions.TradingAction.HOLD],
                     [-0.166668, actions.TradingAction.HOLD],
                     [-0.121212, actions.TradingAction.HOLD],
                     [-0.1, actions.TradingAction.HOLD],
                     [-0.11, actions.TradingAction.HOLD],
                     [-0.478788, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.478789, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_and_down_with_different_and_modified_threshold(self):
        test_detector = detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            0.33, -0.33)
        test_data = [
            [0.0, actions.TradingAction.HOLD],
            [0.15, actions.TradingAction.HOLD],
            [0.3, actions.TradingAction.HOLD],
            [0.4, actions.TradingAction.SWITCH_TO_BEARISH],
            [0.5, actions.TradingAction.HOLD],
            [0.4, actions.TradingAction.HOLD],
            [0.3, actions.TradingAction.HOLD],
            [0.15, actions.TradingAction.HOLD],
            [0.0, actions.TradingAction.HOLD],
            [-0.15, actions.TradingAction.HOLD],
            [-0.3, actions.TradingAction.HOLD],
            [-0.4, actions.TradingAction.SWITCH_TO_BULLISH],
            [-0.5, actions.TradingAction.HOLD],
            [-0.4, actions.TradingAction.HOLD],
            [-0.3, actions.TradingAction.HOLD],
            [-0.15, actions.TradingAction.HOLD],
            [0.0, actions.TradingAction.HOLD],
        ]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))
