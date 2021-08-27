#!/usr/bin/python3

import unittest

import filters.derivative

from config.filter import FilterConfig


class DerivativeTest(unittest.TestCase):
    def test_fill_up(self):
        derivative = filters.derivative.Derivative(FilterConfig({"length": 10}))

        for _ in range(0, 9):
            derivative.put(1.0)
            self.assertIsNone(derivative.get())

        derivative.put(1.0)
        self.assertAlmostEqual(derivative.get(), 0.0)

    def test_delayed_calculation(self):
        derivative = filters.derivative.Derivative(FilterConfig({"length": 10}))

        for i in range(0, 9):
            derivative.put(1.0 if i % 2 else 2.0)
            self.assertIsNone(derivative.get())

        derivative.put(1.0)
        self.assertAlmostEqual(derivative.get(), -1.0)

    def test_zero_derivative(self):
        derivative = filters.derivative.Derivative(FilterConfig({"length": 2}))

        derivative.put(1.0)
        derivative.put(1.0)

        self.assertAlmostEqual(derivative.get(), 0.0)

    def test_increasing_derivative(self):
        derivative = filters.derivative.Derivative(FilterConfig({"length": 2}))

        derivative.put(1.1)
        derivative.put(1.2)

        self.assertAlmostEqual(derivative.get(), 0.1)

    def test_decreasing_derivative(self):
        derivative = filters.derivative.Derivative(FilterConfig({"length": 2}))

        derivative.put(1.2)
        derivative.put(1.1)

        self.assertAlmostEqual(derivative.get(), -0.1)
