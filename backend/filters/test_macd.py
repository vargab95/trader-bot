#!/usr/bin/python3

import unittest

import filters.macd

from config.filter import FilterConfig


class MACDTest(unittest.TestCase):
    def test_fill_up(self):
        macd = filters.macd.MACD(FilterConfig({"length": 5, "second_length": 10}))

        for _ in range(0, 9):
            macd.put(1.0)
            self.assertIsNone(macd.get())

        macd.put(1.0)
        self.assertEqual(macd.get(), 0.0)


if __name__ == "__main__":
    unittest.main()
