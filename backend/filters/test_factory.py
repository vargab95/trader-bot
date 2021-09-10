#!/usr/bin/python3

import unittest

from filters.factory import FilterFactory, InvalidFilterFactoryParameter
import filters.sma
import filters.wma
import filters.hma
import filters.nth
import filters.rsi
import filters.derivative
import filters.derivative_ratio
import filters.complex
import config.filter


class FilterFactoryTest(unittest.TestCase):
    def test_create_sma(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "sma", "length": 4}))
        self.assertIsInstance(instance, filters.sma.SMA)

    def test_create_wma(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "wma", "length": 4}))
        self.assertIsInstance(instance, filters.wma.WMA)

    def test_create_hma(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "hma", "length": 4}))
        self.assertIsInstance(instance, filters.hma.HMA)

    def test_create_derivative(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "derivative", "length": 4}))
        self.assertIsInstance(instance, filters.derivative.Derivative)

    def test_create_derivative_ratio(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "derivative_ratio", "length": 4}))
        self.assertIsInstance(instance, filters.derivative_ratio.DerivativeRatio)

    def test_create_nth(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "nth", "length": 4}))
        self.assertIsInstance(instance, filters.nth.NthFilter)

    def test_create_rsi(self):
        instance = FilterFactory.create(config.filter.FilterConfig({"type": "rsi", "length": 4}))
        self.assertIsInstance(instance, filters.rsi.RSI)

    def test_create_complex(self):
        instance = FilterFactory.create_complex([
            config.filter.FilterConfig({
                "type": "sma",
                "length": 5
            }), config.filter.FilterConfig({
                "type": "derivative",
                "length": 2
            })
        ])
        self.assertIsInstance(instance, filters.complex.Complex)

    def test_create_complex_invalid_type(self):
        with self.assertRaises(InvalidFilterFactoryParameter):
            FilterFactory.create_complex([
                config.filter.FilterConfig({
                    "type": "invalid",
                    "length": 4
                }), config.filter.FilterConfig({
                    "type": "sma",
                    "length": 5
                })
            ])

    def test_create_complex_invalid_length(self):
        with self.assertRaises(InvalidFilterFactoryParameter):
            FilterFactory.create_complex([
                config.filter.FilterConfig({
                    "type": "sma",
                    "length": 5
                }), config.filter.FilterConfig({
                    "type": "derivative",
                    "length": -1
                })
            ])

    def test_invalid_param_filter_type(self):
        with self.assertRaises(InvalidFilterFactoryParameter):
            FilterFactory.create(config.filter.FilterConfig({"type": "invalid", "length": 4}))

    def test_invalid_param_filter_length(self):
        with self.assertRaises(InvalidFilterFactoryParameter):
            FilterFactory.create(config.filter.FilterConfig({"type": "sma", "length": -1}))
