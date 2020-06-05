#!/usr/bin/python3

import unittest

from datetime import datetime

import utils.estimators


class UtilsTest(unittest.TestCase):
    def test_determine_key_value(self):
        self.assertEqual(utils.estimators.determine_key({"value": 1}), "value")

    def test_determine_key_price(self):
        self.assertEqual(utils.estimators.determine_key({"price": 1}), "price")

    def test_calculate_thrid_point(self):
        self.assertEqual(
            round(
                utils.estimators.calculate_third_point(
                    {
                        "date": datetime(2000, 1, 1),
                        "value": 2
                    }, {
                        "date": datetime(2002, 1, 1),
                        "value": 1
                    }, datetime(2001, 1, 1)), 2), 1.5)
