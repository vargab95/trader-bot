#!/usr/bin/python3

import unittest

import detector.moving_threshold
import actions

class SpiderMock:
    def __init__(self):
        self.summary = 0.0

    def get_technical_summary(self) -> float:
        return self.summary

class CrossOverDetectorTest(unittest.TestCase):
    def setUp(self):
        self.spider = SpiderMock()

    def test_quick_fall_down(self):
        test_detector = detector.moving_threshold.MovingThresholdCrossOverDetector(0.0, 0.0, self.spider)
        test_data = [
            [-0.066667, actions.TradingAction.SWITCH_TO_BEARISH],
            [-0.066668, actions.TradingAction.HOLD],
            [-0.021212, actions.TradingAction.HOLD],
            [0.0, actions.TradingAction.HOLD],
            [0.0, actions.TradingAction.HOLD],
            [-0.378788, actions.TradingAction.HOLD],
            [-0.378789, actions.TradingAction.HOLD]
        ]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))
