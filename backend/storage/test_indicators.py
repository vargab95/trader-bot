#!/usr/bin/python3

import unittest
import unittest.mock

import datetime

from signals.trading_signal import TradingSignalPoint, IndicatorSignalDescriptor
from storage.indicators import IndicatorsStorage
from storage.test_mocks import MongoSignalTableMock, MongoSignalResult, DatabaseMock


INDICATOR_DATA = [
    {"value": 1.0, "date": datetime.datetime(2000, 1, 1)},
    {"value": 2.0, "date": datetime.datetime(2000, 1, 2)},
    {"value": 3.0, "date": datetime.datetime(2000, 1, 3)},
    {"value": 4.0, "date": datetime.datetime(2000, 1, 4)},
    {"value": 5.0, "date": datetime.datetime(2000, 1, 5)},
]


class IndicatorsStorageTest(unittest.TestCase):
    def setUp(self):
        self.database = DatabaseMock()
        self.storage = IndicatorsStorage(self.database)
        MongoSignalTableMock.data_to_find = INDICATOR_DATA

    def tearDown(self):
        MongoSignalTableMock.reset()
        MongoSignalResult.reset()

    def test_add(self):
        self.storage.add(
            IndicatorSignalDescriptor(
                market="market", indicator="indicator", candle_size="candle_size"),
            TradingSignalPoint(value=1.0)
        )

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.insert_call_count, 1)
        self.assertTrue(MongoSignalTableMock.last_insert_input["date"])
        self.assertAlmostEqual(
            MongoSignalTableMock.last_insert_input["value"], 1.0)

    def test_add_with_date(self):
        self.storage.add(
            IndicatorSignalDescriptor(
                market="market", indicator="indicator", candle_size="candle_size"),
            TradingSignalPoint(value=1.0, date=datetime.datetime(2000, 1, 1))
        )

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.insert_call_count, 1)
        self.assertEqual(
            MongoSignalTableMock.last_insert_input["date"], datetime.datetime(2000, 1, 1))
        self.assertAlmostEqual(
            MongoSignalTableMock.last_insert_input["value"], 1.0)

    def test_get_all(self):
        result = self.storage.get(IndicatorSignalDescriptor(
            market="market", indicator="indicator", candle_size="candle_size"))

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, indicator in enumerate(INDICATOR_DATA):
            self.assertEqual(
                result.data[i].date, indicator["date"])
            self.assertAlmostEqual(
                result.data[i].value, indicator["value"])

        self.assertEqual(MongoSignalTableMock.last_find_request, None)
        self.assertEqual(MongoSignalResult.limit_call_count, 0)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)

    def test_get_from_start_date(self):
        result = self.storage.get(IndicatorSignalDescriptor(
            market="market",
            start_date=datetime.datetime(1999, 1, 1),
            indicator="indicator",
            candle_size="candle_size"
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, indicator in enumerate(INDICATOR_DATA):
            self.assertEqual(
                result.data[i].date, indicator["date"])
            self.assertAlmostEqual(
                result.data[i].value, indicator["value"])

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
        result = self.storage.get(IndicatorSignalDescriptor(
            market="market",
            end_date=datetime.datetime(1999, 1, 1),
            indicator="indicator",
            candle_size="candle_size"
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, indicator in enumerate(INDICATOR_DATA):
            self.assertEqual(
                result.data[i].date, indicator["date"])
            self.assertAlmostEqual(
                result.data[i].value, indicator["value"])

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
        result = self.storage.get(IndicatorSignalDescriptor(
            market="market",
            start_date=datetime.datetime(1999, 1, 1),
            end_date=datetime.datetime(1999, 1, 1),
            indicator="indicator",
            candle_size="candle_size"
        ))

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i, indicator in enumerate(INDICATOR_DATA):
            self.assertEqual(
                result.data[i].date, indicator["date"])
            self.assertAlmostEqual(
                result.data[i].value, indicator["value"])

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
            IndicatorSignalDescriptor(market="market", limit=2, indicator="indicator", candle_size="candle_size"))

        self.assertEqual(MongoSignalTableMock.table_name, "candle_size")
        self.assertEqual(MongoSignalTableMock.find_call_count, 1)

        for i in range(2):
            self.assertEqual(
                result.data[i].date, INDICATOR_DATA[i]["date"])
            self.assertAlmostEqual(
                result.data[i].value, INDICATOR_DATA[i]["value"])

        self.assertEqual(MongoSignalTableMock.last_find_request, None)
        self.assertEqual(MongoSignalResult.limit_call_count, 1)
        self.assertEqual(MongoSignalResult.sort_call_count, 1)
