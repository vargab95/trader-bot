#!/usr/bin/python3

import unittest
import unittest.mock

import storage.client
import pymongo


class ClientMock:
    trading_view_bot = "The database"


class StorageClientTest(unittest.TestCase):
    @unittest.mock.patch("pymongo.MongoClient", return_value=ClientMock())
    def test_get_database(self, client_mock):
        self.assertEqual(ClientMock.trading_view_bot,
                         storage.client.Client("", "", "").database)
