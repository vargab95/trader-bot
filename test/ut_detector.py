import unittest
import enum

import detector

class CurrencyState(enum.Enum):
    NONE = 0
    BULL = 1
    BEAR = 2

CURRENT_STATE: CurrencyState = CurrencyState.NONE

def bear():
    global CURRENT_STATE
    CURRENT_STATE = CurrencyState.BEAR

def bull():
    global CURRENT_STATE
    CURRENT_STATE = CurrencyState.BULL

class CrossOverDetectorTest(unittest.TestCase):
    def setUp(self):
        self.detector = detector.CrossOverDetector(bull, bear)

    def test_fall_down(self):
        test_data = [
            [-0.066667, CurrencyState.BEAR],
            [-0.066667, CurrencyState.BEAR],
            [-0.021212, CurrencyState.BEAR],
            [0.0, CurrencyState.BULL],
            [0.0, CurrencyState.BULL],
            [-0.378788, CurrencyState.BEAR],
            [-0.378788, CurrencyState.BEAR]
        ]
        for line in test_data:
            self.detector.check_crossover(line[0])
            self.assertEqual(CURRENT_STATE, line[1])
