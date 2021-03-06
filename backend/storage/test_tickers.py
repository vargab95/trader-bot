#!/usr/bin/python3

import unittest
import unittest.mock

import datetime

from signals.trading_signal import TradingSignalPoint, TickerSignalDescriptor
from storage.tickers import TickersStorage
from storage.test_mocks import MongoSignalTableMock, MongoSignalResult, DatabaseMock


TICKER_DATA = [
    {"price": 1.0, "date": datetime.datetime(2000, 1, 1)},
    {"price": 2.0, "date": datetime.datetime(2000, 1, 2)},
    {"price": 3.0, "date": datetime.datetime(2000, 1, 3)},
    {"price": 4.0, "date": datetime.datetime(2000, 1, 4)},
    {"price": 5.0, "date": datetime.datetime(2000, 1, 5)},
]


class TickersStorageTest(unittest.TestCase):
    def setUp(self):
        self.database = DatabaseMock()
        self.storage = TickersStorage(self.database)
        MongoSignalTableMock.data_to_find = TICKER_DATA

    def tearDown(self):
        MongoSignalTableMock.reset()
        MongoSignalResult.reset()

    def test_add(self):
        self.storage.add(
            TickerSignalDescriptor(market="market"),
            TradingSignalPoint(value=1.0)
        )

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.insert_call_count, 1)
        self.assertTrue(MongoSignalTableMock.last_insert_input["date"])
        self.assertAlmostEqual(
            MongoSignalTableMock.last_insert_input["price"], 1.0)

    def test_add_with_date(self):
        self.storage.add(
            TickerSignalDescriptor(market="market"),
            TradingSignalPoint(value=1.0, date=datetime.datetime(2000, 1, 1))
        )

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.insert_call_count, 1)
        self.assertEqual(
            MongoSignalTableMock.last_insert_input["date"], datetime.datetime(2000, 1, 1))
        self.assertAlmostEqual(
            MongoSignalTableMock.last_insert_input["price"], 1.0)

    def test_get_all(self):
        result = self.storage.get(TickerSignalDescriptor(market="market"))

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, ticker in enumerate(TICKER_DATA):
            self.assertEqual(
                result.data[i].date, ticker["date"])
            self.assertAlmostEqual(
                result.data[i].value, ticker["price"])

        self.assertEqual(MongoSignalTableMock.last_find_request, None)
        self.assertEqual(MongoSignalResult.limit_call_count, 0)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)

    def test_get_from_start_date(self):
        result = self.storage.get(TickerSignalDescriptor(
            market="market",
            start_date=datetime.datetime(1999, 1, 1)
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, ticker in enumerate(TICKER_DATA):
            self.assertEqual(
                result.data[i].date, ticker["date"])
            self.assertAlmostEqual(
                result.data[i].value, ticker["price"])

        self.assertEqual(
            MongoSignalTableMock.last_find_request,
            {
                'date': {
                    '$gte': datetime.datetime(1999, 1, 1, 0, 0)
                }
            }
        )
        self.assertEqual(MongoSignalResult.limit_call_count, 0)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)

    def test_get_to_end_date(self):
        result = self.storage.get(TickerSignalDescriptor(
            market="market",
            end_date=datetime.datetime(1999, 1, 1)
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, ticker in enumerate(TICKER_DATA):
            self.assertEqual(
                result.data[i].date, ticker["date"])
            self.assertAlmostEqual(
                result.data[i].value, ticker["price"])

        self.assertEqual(
            MongoSignalTableMock.last_find_request,
            {
                'date': {
                    '$lt': datetime.datetime(1999, 1, 1, 0, 0)
                }
            }
        )
        self.assertEqual(MongoSignalResult.limit_call_count, 0)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)

    def test_get_between_dates(self):
        result = self.storage.get(TickerSignalDescriptor(
            market="market",
            start_date=datetime.datetime(1999, 1, 1),
            end_date=datetime.datetime(1999, 1, 1)
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, ticker in enumerate(TICKER_DATA):
            self.assertEqual(
                result.data[i].date, ticker["date"])
            self.assertAlmostEqual(
                result.data[i].value, ticker["price"])

        self.assertEqual(MongoSignalTableMock.last_find_request, {
            'date': {
                '$gte': datetime.datetime(1999, 1, 1, 0, 0),
                '$lt': datetime.datetime(1999, 1, 1, 0, 0)
            }
        })
        self.assertEqual(MongoSignalResult.limit_call_count, 0)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)

    def test_get_with_limit(self):
        result = self.storage.get(
            TickerSignalDescriptor(market="market", limit=2))

        self.assertEqual(MongoSignalTableMock.table_name, "market")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i in range(2):
            self.assertEqual(
                result.data[i].date, TICKER_DATA[i]["date"])
            self.assertAlmostEqual(
                result.data[i].value, TICKER_DATA[i]["price"])

        self.assertEqual(MongoSignalTableMock.last_find_request, None)
        self.assertEqual(MongoSignalResult.limit_call_count, 1)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)
