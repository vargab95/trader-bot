#!/usr/bin/python3

import unittest

import filters.sma


class SMATest(unittest.TestCase):
    def test_fill_up(self):
        sma = filters.sma.SMA(10)

        for _ in range(0, 9):
            sma.put(1.0)
            self.assertIsNone(sma.get())

        sma.put(1.0)
        self.assertEqual(sma.get(), 1.0)

    def test_calculation(self):
        sma = filters.sma.SMA(10)

        for i in range(0, 9):
            sma.put(1.0 if i % 2 else 2.0)
            self.assertIsNone(sma.get())

        sma.put(1.0)
        self.assertEqual(sma.get(), 1.5)
