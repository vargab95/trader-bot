#!/usr/bin/python3

import unittest

import binance.exceptions

import exchange.guard


class response_mock:
    status_code = 1

    @staticmethod
    def json():
        return {"code": "1", "msg": "1"}


class ExchangeGuardTest(unittest.TestCase):
    @exchange.guard.exchange_guard
    def test_function(self):
        if self.raise_until > 0:
            self.raise_until -= 1
            raise binance.exceptions.BinanceAPIException(response_mock())
        return True

    def setUp(self):
        self.raise_until = -1

    def test_normal_flow(self):
        self.assertTrue(self.test_function())

    def test_temporary_failure(self):
        self.raise_until = 10
        self.assertTrue(self.test_function())

    def test_permanent_failure(self):
        self.raise_until = 33
        self.assertFalse(self.test_function())
