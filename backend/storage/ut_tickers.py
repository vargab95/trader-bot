#!/usr/bin/python3

import unittest

import storage.tickers
import storage.client


class TickersTest(unittest.TestCase):
    def setUp(self):
        self.database = storage.client.Client("", "", "").database
        self.storage = storage.tickers.TickersStorage(self.database)

    def test_add_some_data(self):
        self.storage.add("test", 1.1)
        self.storage.add("test", 1.2)
        self.storage.add("test", 1.3)
        self.storage.add("test", 1.4)
