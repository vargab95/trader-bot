#!/usr/bin/python3

import unittest

from .rsi import RSI


class TestRSIFilter(unittest.TestCase):
    def test_rsi(self):
        filt = RSI(14)

        for i in [12, 11, 12, 14, 18, 12, 15, 13, 16, 12, 11, 13, 15, 14, 16, 18, 22, 19, 24, 17, 19]:
            filt.put(i)

        self.assertAlmostEqual(filt.get(), 55.23, 2)
