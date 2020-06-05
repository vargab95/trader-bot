#!/usr/bin/python3

import unittest

import filters.wma


class WMATest(unittest.TestCase):
    def test_fill_up(self):
        wma = filters.wma.WMA(10)

        for _ in range(0, 9):
            wma.put(1.0)
            self.assertIsNone(wma.get())

        wma.put(1.0)
        self.assertEqual(wma.get(), 1.0)

    def test_calculation(self):
        wma = filters.wma.WMA(5)

        wma.put(16.0)
        wma.put(17.0)
        wma.put(17.0)
        wma.put(10.0)
        wma.put(17.0)

        self.assertAlmostEqual(round(wma.get(), 2), 15.07)
