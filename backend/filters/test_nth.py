#!/usr/bin/python3

import unittest

import filters.nth


class NthFilterTest(unittest.TestCase):
    def test_fill_up(self):
        nth = filters.nth.NthFilter(10)

        for _ in range(0, 9):
            nth.put(1.0)
            self.assertIsNone(nth.get())

        nth.put(1.0)
        self.assertEqual(nth.get(), 1.0)

    def test_calculation(self):
        nth = filters.nth.NthFilter(2)

        nth.put(1)
        self.assertEqual(nth.get(), None)

        nth.put(2)
        self.assertEqual(nth.get(), 2)

        nth.put(3)
        self.assertEqual(nth.get(), 2)

        nth.put(4)
        self.assertEqual(nth.get(), 4)
