#!/usr/bin/python3

import unittest
import unittest.mock

import storage.client


class ClientMock:
    trading_view_bot = "The database"


class StorageClientTest(unittest.TestCase):
    @unittest.mock.patch("pymongo.MongoClient", return_value=ClientMock())
    def test_get_database(self, _):
        self.assertEqual(ClientMock.trading_view_bot,
                         storage.client.Client("", "", "").database)
