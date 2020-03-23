#!/usr/bin/python3

import unittest

import detector.moving_threshold
import actions


class FetcherMock:
    def __init__(self):
        self.indicator = 0.0

    def fetch_technical_indicator(self):
        pass

    def get_technical_indicator(self) -> float:
        return self.indicator


class RisingEdgeDetectorTest(unittest.TestCase):
    def setUp(self):
        self.gatherer = FetcherMock()

    def test_quick_fall_down_zero_threshold(self):
        test_detector = \
                detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                    0.0, 0.0, self.gatherer)
        test_data = [[-0.066667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [-0.066668, actions.TradingAction.HOLD],
                     [-0.021212, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [-0.378788, actions.TradingAction.HOLD],
                     [-0.378789, actions.TradingAction.HOLD]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_below_threshold(self):
        test_detector = \
                detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                    0.0, 0.0, self.gatherer)
        test_data = [[-0.066667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [-0.066668, actions.TradingAction.HOLD],
                     [-0.021212, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [-0.378788, actions.TradingAction.HOLD],
                     [-0.378789, actions.TradingAction.HOLD]]

        self.gatherer.indicator = -0.1

        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_above_threshold(self):
        test_detector = \
                detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                    0.0, 0.0, self.gatherer)
        test_data = [[-0.066667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.066668, actions.TradingAction.HOLD],
                     [-0.021212, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [0.0, actions.TradingAction.HOLD],
                     [-0.378788, actions.TradingAction.SWITCH_TO_BEARISH],
                     [-0.378789, actions.TradingAction.HOLD]]

        self.gatherer.indicator = 0.1

        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_move_threshold_above_bullish_while_in_bear(self):
        test_detector = \
                detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                    0.0, 0.0, self.gatherer)
        test_data = [[0.0, 0.066667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [0.0, 0.166667, actions.TradingAction.HOLD],
                     [-0.3, 0.266667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [-0.3, 0.276667, actions.TradingAction.HOLD],
                     [-0.3, 0.366667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [-0.3, 0.466667, actions.TradingAction.HOLD]]

        for line in test_data:
            self.gatherer.indicator = line[0]
            self.assertEqual(test_detector.check(line[1]), line[2], str(line))

    def test_move_threshold_below_bearish_while_in_bull(self):
        test_detector = \
                detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                    0.0, 0.0, self.gatherer)
        test_data = [[0.0, -0.066667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [0.0, -0.166667, actions.TradingAction.HOLD],
                     [0.3, -0.266667, actions.TradingAction.SWITCH_TO_BULLISH],
                     [0.3, -0.276667, actions.TradingAction.HOLD],
                     [0.3, -0.366667, actions.TradingAction.SWITCH_TO_BEARISH],
                     [0.3, -0.466667, actions.TradingAction.HOLD]]

        for line in test_data:
            self.gatherer.indicator = line[0]
            self.assertEqual(test_detector.check(line[1]), line[2], str(line))
