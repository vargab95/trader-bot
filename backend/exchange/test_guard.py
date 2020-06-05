#!/usr/bin/python3

import unittest

import binance.exceptions

import exchange.guard


class ResponseMock:
    status_code = 1

    @staticmethod
    def json():
        return {"code": "1", "msg": "1"}


class ExchangeGuardTest(unittest.TestCase):
    @exchange.guard.exchange_guard(0)
    def function(self):
        if self.raise_until > 0:
            self.raise_until -= 1
            raise binance.exceptions.BinanceAPIException(ResponseMock())
        return True

    def setUp(self):
        self.raise_until = -1

    def test_normal_flow(self):
        self.assertTrue(self.function())

    def test_failure(self):
        self.raise_until = 2
        self.assertTrue(self.function())
