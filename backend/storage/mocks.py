#!/usr/bin/python3

import pymongo.errors


class MongoUserTableMock:
    insert_call_count = 0
    find_call_count = 0
    simulate_duplicate = False

    def insert_one(self, _):
        MongoUserTableMock.insert_call_count += 1
        if self.simulate_duplicate:
            raise pymongo.errors.DuplicateKeyError("A")

    @staticmethod
    def find_one(_):
        MongoUserTableMock.find_call_count += 1

    @classmethod
    def reset(cls):
        cls.find_call_count = 0
        cls.insert_call_count = 0
        cls.simulate_duplicate = False


class MongoSignalIterator:
    def __init__(self, data):
        self.data = data
        self.index = -1

    def __next__(self):
        self.index += 1
        if self.index < len(self.data):
            return self.data[self.index] if isinstance(self.data, list) else self.data.data[self.index]
        raise StopIteration


class MongoSignalResult:
    sort_call_count = 0
    limit_call_count = 0

    def __init__(self, data):
        self.data = data

    def limit(self, limit):
        MongoSignalResult.limit_call_count += 1
        if len(self.data) > limit:
            return self.data[:limit]
        return self.data

    def sort(self, key):
        MongoSignalResult.sort_call_count += 1
        return self

    def __iter__(self):
        return MongoSignalIterator(self.data)

    @classmethod
    def reset(cls):
        cls.sort_call_count = 0
        cls.limit_call_count = 0


class MongoSignalTableMock:
    last_insert_input = {}
    last_find_request = {}
    data_to_find = None
    insert_call_count = 0
    find_call_count = 0
    table_name = ""

    def __init__(self, key=""):
        MongoSignalTableMock.table_name = key

    @classmethod
    def insert_one(cls, ticker):
        cls.last_insert_input = ticker
        cls.insert_call_count += 1

    @classmethod
    def find(cls, request=None):
        cls.last_find_request = request
        cls.find_call_count += 1
        return MongoSignalResult(cls.data_to_find)

    def __getitem__(self, key):
        return MongoSignalTableMock(key)

    @classmethod
    def reset(cls):
        cls.last_insert_input = {}
        cls.last_find_request = {}
        cls.data_to_find = None
        cls.insert_call_count = 0
        cls.find_call_count = 0
        cls.sort_call_count = 0
        cls.limit_call_count = 0
        cls.table_name = ""


class DatabaseMock:
    @property
    def users(self):
        return MongoUserTableMock()

    @property
    def tickers(self):
        return MongoSignalTableMock()

    @property
    def indicators(self):
        return MongoSignalTableMock()
