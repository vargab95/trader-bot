#!/usr/bin/python3

import unittest
import unittest.mock

import pymongo.errors

import storage.user


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


class DatabaseMock:
    @property
    def users(self):
        return MongoUserTableMock()


class UserStorageTest(unittest.TestCase):
    def setUp(self):
        MongoUserTableMock.find_call_count = 0
        MongoUserTableMock.insert_call_count = 0
        MongoUserTableMock.simulate_duplicate = False

    def test_insert_pass(self):
        store = storage.user.UserStorage(DatabaseMock())
        store.add("a@a.a", "abcd")
        self.assertEqual(1, MongoUserTableMock.insert_call_count)

    def test_insert_duplicate(self):
        MongoUserTableMock.simulate_duplicate = True
        store = storage.user.UserStorage(DatabaseMock())
        try:
            store.add("a@a.a", "abcd")
            self.fail()
        except storage.user.InvalidUserRequest:
            pass
        self.assertEqual(1, MongoUserTableMock.insert_call_count)

    def test_find_user(self):
        store = storage.user.UserStorage(DatabaseMock())
        store.get("a@a.a")
        self.assertEqual(1, MongoUserTableMock.find_call_count)
