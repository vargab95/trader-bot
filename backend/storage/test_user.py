#!/usr/bin/python3

import unittest
import unittest.mock

import storage.user
from storage.test_mocks import MongoUserTableMock, DatabaseMock


class UserStorageTest(unittest.TestCase):
    def setUp(self):
        MongoUserTableMock.reset()

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
