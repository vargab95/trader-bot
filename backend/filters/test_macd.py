#!/usr/bin/python3

import unittest

import filters.macd

from config.filter import FilterConfig


class MACDTest(unittest.TestCase):
    def test_fill_up(self):
        macd = filters.macd.MACD(FilterConfig({"length": 5, "second_length": 10}))

        for _ in range(0, 19):
            macd.put(1.0)
            self.assertIsNone(macd.get())

        macd.put(1.0)
        self.assertEqual(macd.get(), 0.0)

    def test_calculation(self):
        macd = filters.macd.MACD(FilterConfig({"length": 3, "second_length": 5}))
        data = [
            (11.0, None),
            (12.0, None),
            (9.0, None),
            (13.0, None),
            (10.0, None),
            (17.0, None),
            (15.0, None),
            (13.0, None),
            (9.0, None),
            (7.0, -1.13),
            (5.0, -1.44),
            (3.0, -1.64),
            (1.0, -1.76),
            (0.0, -1.67)
        ]

        for i, output in data:
            macd.put(i)
            self.assertAlmostEqual(macd.get(), output, 2)


if __name__ == "__main__":
    unittest.main()
