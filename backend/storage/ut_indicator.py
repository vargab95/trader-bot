#!/usr/bin/python3

import unittest

import storage.indicators
import storage.client


class TickersTest(unittest.TestCase):
    def setUp(self):
        self.database = storage.client.Client("", "", "").database
        self.storage = storage.indicators.IndicatorsStorage(self.database)

    def test_add_some_data(self):
        self.storage.add("test", "all", "5m", 1.1)
        self.storage.add("test", "all", "5m", 1.2)
        self.storage.add("test", "all", "15m", 1.3)
        self.storage.add("test", "all", "15m", 1.4)
