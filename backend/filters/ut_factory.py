#!/usr/bin/python3

import unittest

import filters.factory
import filters.sma
import filters.wma
import filters.hma
import filters.derivative
import filters.complex


class FilterFactoryTest(unittest.TestCase):
    def test_create_sma(self):
        instance = filters.factory.FilterFactory.create("sma")
        self.assertTrue(isinstance(instance, filters.sma.SMA))

    def test_create_wma(self):
        instance = filters.factory.FilterFactory.create("wma")
        self.assertTrue(isinstance(instance, filters.wma.WMA))

    def test_create_hma(self):
        instance = filters.factory.FilterFactory.create("hma")
        self.assertTrue(isinstance(instance, filters.hma.HMA))

    def test_create_derivative(self):
        instance = filters.factory.FilterFactory.create("derivative")
        self.assertTrue(isinstance(instance, filters.derivative.Derivative))

    def test_create_complex(self):
        instance = filters.factory.FilterFactory.create_complex({
            "sma": 5,
            "derivative": 2
        })
        self.assertTrue(isinstance(instance, filters.complex.Complex))

    def test_create_complex_invalid_type(self):
        try:
            filters.factory.FilterFactory.create_complex({
                "invalid": 4,
                "sma": 5
            })
            self.fail()
        except filters.factory.InvalidFilterFactoryParameter:
            pass

    def test_create_complex_invalid_length(self):
        try:
            filters.factory.FilterFactory.create_complex({
                "sma": 5,
                "derivative": -1
            })
            self.fail()
        except filters.factory.InvalidFilterFactoryParameter:
            pass

    def test_invalid_param_filter_type(self):
        try:
            filters.factory.FilterFactory.create("invalid")
            self.fail()
        except filters.factory.InvalidFilterFactoryParameter:
            pass

    def test_invalid_param_filter_length(self):
        try:
            filters.factory.FilterFactory.create("sma", -1)
            self.fail()
        except filters.factory.InvalidFilterFactoryParameter:
            pass
