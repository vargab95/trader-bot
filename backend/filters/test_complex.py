#!/usr/bin/python3

import unittest

import filters.complex
import filters.sma
import filters.wma
import filters.hma
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

    def test_with_real_values(self):
        test_data = [418.9, 424.1, 417.7, 418.3, 417.1, 418.8, 418.8, 417.0, 416.8, 417.1, 418.8, 418.8,
                     418.8, 414.5, 416.6, 409.9, 406.4, 404.7, 408.4, 416.0, 412.2, 414.8, 413.7, 415.6,
                     416.6, 420.5, 425.5, 427.6, 428.9, 430.0, 430.6, 433.7, 430.0, 425.2, 432.3, 432.4,
                     435.5, 433.6, 432.4, 432.4, 434.4, 436.3, 439.4, 442.2, 442.2, 442.2, 442.2, 444.6,
                     442.2, 442.2, 440.3, 438.2, 422.9, 406.5, 404.9, 411.1, 405.1, 409.7, 417.6, 418.9]

        complex_filter = filters.complex.Complex()

        complex_filter.add_filter(filters.hma.HMA(42))
        complex_filter.add_filter(filters.derivative.Derivative(2))
        complex_filter.add_filter(filters.wma.WMA(4))

        for data in test_data:
            complex_filter.put(data)

        self.assertAlmostEqual(complex_filter.get(), -3.183375904)
