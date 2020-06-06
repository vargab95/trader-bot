#!/usr/bin/python3

import unittest

from datetime import datetime

import utils.estimators
from signals.trading_signal import TradingSignalPoint


class UtilsTest(unittest.TestCase):
    def test_calculate_thrid_point(self):
        self.assertEqual(
            round(
                utils.estimators.calculate_third_point(
                    TradingSignalPoint(date=datetime(2000, 1, 1), value=2),
                    TradingSignalPoint(date=datetime(2002, 1, 1), value=1),
                    datetime(2001, 1, 1)), 2), 1.5)
