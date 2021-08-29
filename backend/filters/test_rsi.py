#!/usr/bin/python3

import unittest

from config.filter import FilterConfig

from filters.rsi import RSI


class TestRSIFilter(unittest.TestCase):
    def test_rsi(self):
        filt = RSI(FilterConfig({"length": 14}))

        for i in [12, 11, 12, 14, 18, 12, 15, 13, 16, 12, 11, 13, 15, 14, 16, 18, 22, 19, 24, 17, 19]:
            filt.put(i)

        self.assertAlmostEqual(filt.get(), 55.23, 2)

    def test_rsi_on_constant(self):
        filt = RSI(FilterConfig({"length": 7}))

        for i in [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]:
            filt.put(i)

        self.assertEqual(filt.get(), None)


if __name__ == "__main__":
    unittest.main()
