#!/usr/bin/python3

import unittest

import filters.hma

from config.filter import FilterConfig


class HMATest(unittest.TestCase):
    def test_fill_up(self):
        hma = filters.hma.HMA(FilterConfig({"length": 10}))

        for _ in range(0, 11):
            hma.put(1.0)
            self.assertIsNone(hma.get())

        hma.put(1.0)
        self.assertEqual(hma.get(), 1.0)

    def test_calculation_linear(self):
        hma = filters.hma.HMA(FilterConfig({"length": 9}))

        for i in range(20, 31):
            hma.put(i)

        self.assertAlmostEqual(round(hma.get(), 2), 30.0)

    def test_calculation(self):
        hma = filters.hma.HMA(FilterConfig({"length": 9}))

        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(0)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(10)
        hma.put(0)
        hma.put(0)

        self.assertAlmostEqual(round(hma.get(), 2), 3.48)
