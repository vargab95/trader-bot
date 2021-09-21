#!/usr/bin/python3

import unittest

import filters.ema

from config.filter import FilterConfig


class EMATest(unittest.TestCase):
    def test_fill_up(self):
        ema = filters.ema.EMA(FilterConfig({"length": 10}))

        for _ in range(0, 9):
            ema.put(1.0)
            self.assertIsNone(ema.get())

        ema.put(1.0)
        self.assertEqual(ema.get(), 1.0)

    def test_calculation_2(self):
        ema = filters.ema.EMA(FilterConfig({"length": 10}))
        data = [
            (22.27, None),
            (22.19, None),
            (22.08, None),
            (22.17, None),
            (22.18, None),
            (22.13, None),
            (22.23, None),
            (22.43, None),
            (22.24, None),
            (22.29, 22.22),
            (22.15, 22.21),
            (22.39, 22.24),
            (22.38, 22.27),
            (22.61, 22.33),
            (23.36, 22.52),
            (24.05, 22.80),
            (23.75, 22.97),
            (23.83, 23.13),
            (23.95, 23.28),
            (23.63, 23.34),
            (23.82, 23.43),
            (23.87, 23.51),
            (23.65, 23.53),
            (23.19, 23.47),
            (23.10, 23.40),
            (23.33, 23.39),
            (22.68, 23.26),
            (23.10, 23.23),
            (22.40, 23.08),
            (22.17, 22.92)
        ]

        for i, output in data:
            ema.put(i)
            self.assertAlmostEqual(ema.get(), output, 2)


if __name__ == "__main__":
    unittest.main()
