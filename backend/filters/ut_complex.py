#!/usr/bin/python3

import unittest

import filters.complex
import filters.sma
import filters.wma
import filters.derivative


class ComplexTest(unittest.TestCase):
    def test_fill_up(self):
        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.sma.SMA(10))
        complex_filter.add_filter(filters.sma.SMA(10))

        for _ in range(0, 18):
            complex_filter.put(1.0)
            self.assertIsNone(complex_filter.get())

        complex_filter.put(1.0)
        self.assertEqual(complex_filter.get(), 1.0)

    def test_length_property(self):
        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.sma.SMA(10))
        complex_filter.add_filter(filters.wma.WMA(10))

        for _ in range(0, 20):
            complex_filter.put(1.0)

        self.assertEqual(complex_filter.length, 20)

    def test_all_property(self):
        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.wma.WMA(10))
        complex_filter.add_filter(filters.wma.WMA(10))

        self.assertEqual(complex_filter.all, None)

    def test_no_filter_specified(self):
        complex_filter = filters.complex.Complex()

        try:
            complex_filter.get()
            self.fail()
        except filters.complex.NoFilterSpecified:
            pass

    def test_simple_calculation(self):
        test_data = [
            1.5, 1.2, 4.3, 56.4, 3.2, 5.7, 4.3, 8.5, 3.4, 6.5, 4.3, 6.8, 9.5,
            4.3, 14.3, 34.2, 1.32, 3.4, 3.2, 6.7, 2.4, 0.0, -1.5, 3.5, 3.2
        ]

        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.sma.SMA(5))
        sma = filters.sma.SMA(5)

        for data in test_data:
            sma.put(data)
            complex_filter.put(data)
            self.assertAlmostEqual(sma.get(), complex_filter.get())

    def test_complex_calculation(self):
        test_data = [
            1.5, 1.2, 4.3, 56.4, 3.2, 5.7, 4.3, 8.5, 3.4, 6.5, 4.3, 6.8, 9.5,
            4.3, 14.3, 34.2, 1.32, 3.4, 3.2, 6.7, 2.4, 0.0, -1.5, 3.5, 3.2
        ]

        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.sma.SMA(5))
        complex_filter.add_filter(filters.derivative.Derivative(2))
        sma = filters.sma.SMA(5)
        deriv = filters.derivative.Derivative(2)

        for data in test_data:
            sma.put(data)
            if sma.get() is not None:
                deriv.put(sma.get())

            complex_filter.put(data)

            if deriv.get():
                self.assertAlmostEqual(deriv.get(), complex_filter.get())
