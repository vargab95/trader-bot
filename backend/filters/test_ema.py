#!/usr/bin/python3

import unittest

import filters.ema

from config.filter import FilterConfig


class EMATest(unittest.TestCase):
    def test_fill_up(self):
        ema = filters.ema.EMA(FilterConfig({"length": 10}))

        for _ in range(0, 19):
            ema.put(1.0)
            self.assertIsNone(ema.get())

        ema.put(1.0)
        self.assertEqual(ema.get(), 1.0)

    def test_calculation(self):
        ema = filters.ema.EMA(FilterConfig({"length": 5}))
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
            (7.0, 10.31),
            (5.0, 8.53),
            (3.0, 6.68),
            (1.0, 4.78),
            (0.0, 3.18)
        ]

        for i, output in data:
            ema.put(i)
            self.assertAlmostEqual(ema.get(), output, 2)


if __name__ == "__main__":
    unittest.main()
