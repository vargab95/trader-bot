import unittest

from detector.latched_rising_edge import LatchedRisingEdgeDetector
import detector.common


class LatchedRisingEdgeDetectorTest(unittest.TestCase):
    def test_oscillate_at_bull(self):
        test_detector = LatchedRisingEdgeDetector(-0.1, 0.1)
        test_data = [[0.166667, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.066668, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.121212, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.021212, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.1, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.178788, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.078789, detector.common.TradingAction.BULLISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_oscillate_at_bear(self):
        test_detector = LatchedRisingEdgeDetector(-0.1, 0.1)
        test_data = [[-0.166667, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.066668, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.121212, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.021212, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.1, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.178788, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.078789, detector.common.TradingAction.BEARISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down(self):
        test_detector = LatchedRisingEdgeDetector(0.0, 0.0)
        test_data = [[-0.066667, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.066668, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.021212, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.0, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.0, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.378788, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.378789, detector.common.TradingAction.BEARISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_slow_up_trend(self):
        test_detector = LatchedRisingEdgeDetector(0.0, 0.0)
        test_data = [[-0.045455, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.045456, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.045457, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.066667, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.0, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.01, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.02, detector.common.TradingAction.BULLISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_trend_with_same_but_modified_threshold(self):
        test_detector = LatchedRisingEdgeDetector(0.1, 0.1)
        test_data = [[-0.145455, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.145456, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.145457, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.166667, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.1, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.11, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.12, detector.common.TradingAction.BULLISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_with_same_but_modified_threshold(self):
        test_detector = LatchedRisingEdgeDetector(-0.1, -0.1)
        test_data = [[-0.166667, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.166668, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.121212, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.1, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.11, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.478788, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.478789, detector.common.TradingAction.BEARISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_trend_with_different_and_modified_threshold(self):
        test_detector = LatchedRisingEdgeDetector(-0.1, 0.1)
        test_data = [[-0.15, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.1, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.05, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.0, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.05, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.1, detector.common.TradingAction.BEARISH_SIGNAL],
                     [0.166667, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.1, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.11, detector.common.TradingAction.BULLISH_SIGNAL],
                     [0.12, detector.common.TradingAction.BULLISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_quick_fall_down_with_different_and_modified_threshold(self):
        test_detector = LatchedRisingEdgeDetector(-0.33, 0.33)
        test_data = [[-0.166667, detector.common.TradingAction.HOLD_SIGNAL],
                     [-0.166668, detector.common.TradingAction.HOLD_SIGNAL],
                     [-0.121212, detector.common.TradingAction.HOLD_SIGNAL],
                     [-0.1, detector.common.TradingAction.HOLD_SIGNAL],
                     [-0.11, detector.common.TradingAction.HOLD_SIGNAL],
                     [-0.478788, detector.common.TradingAction.BEARISH_SIGNAL],
                     [-0.478789, detector.common.TradingAction.BEARISH_SIGNAL]]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))

    def test_up_and_down_with_different_and_modified_threshold(self):
        test_detector = LatchedRisingEdgeDetector(-0.33, 0.33)
        test_data = [
            [0.0, detector.common.TradingAction.HOLD_SIGNAL],
            [0.15, detector.common.TradingAction.HOLD_SIGNAL],
            [0.3, detector.common.TradingAction.HOLD_SIGNAL],
            [0.4, detector.common.TradingAction.BULLISH_SIGNAL],
            [0.5, detector.common.TradingAction.BULLISH_SIGNAL],
            [0.4, detector.common.TradingAction.BULLISH_SIGNAL],
            [0.3, detector.common.TradingAction.BULLISH_SIGNAL],
            [0.15, detector.common.TradingAction.BULLISH_SIGNAL],
            [0.0, detector.common.TradingAction.BULLISH_SIGNAL],
            [-0.15, detector.common.TradingAction.BULLISH_SIGNAL],
            [-0.3, detector.common.TradingAction.BULLISH_SIGNAL],
            [-0.4, detector.common.TradingAction.BEARISH_SIGNAL],
            [-0.5, detector.common.TradingAction.BEARISH_SIGNAL],
            [-0.4, detector.common.TradingAction.BEARISH_SIGNAL],
            [-0.3, detector.common.TradingAction.BEARISH_SIGNAL],
            [-0.15, detector.common.TradingAction.BEARISH_SIGNAL],
            [0.0, detector.common.TradingAction.BEARISH_SIGNAL],
        ]
        for line in test_data:
            self.assertEqual(test_detector.check(line[0]), line[1], str(line))
