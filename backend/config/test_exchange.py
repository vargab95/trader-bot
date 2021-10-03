import unittest

from config.common import InvalidConfigurationException
from config.exchange import ExchangeConfig


class TestExchangeConfig(unittest.TestCase):
    def setUp(self):
        self.conf = ExchangeConfig({})
        self.conf.id = "id"
        self.conf.name = "ftx"
        self.conf.public_key = "public_key"
        self.conf.private_key = "private_key"
        self.conf.market_name_format = "market_name_format"
        self.conf.start_money = 100.0
        self.conf.base_asset = "USDT"
        self.conf.real_time = True
        self.conf.fee = 0.01
        self.conf.balance_precision = 0.00001
        self.conf.leverage = 1.0

    def test_no_id(self):
        self.conf.id = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_name(self):
        self.conf.name = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_invalid_name(self):
        self.conf.name = "invalid"
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_public_key(self):
        self.conf.public_key = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_private_key(self):
        self.conf.private_key = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_dict_generation(self):
        self.assertDictEqual(self.conf.dict(), {
            "id": "id",
            "name": "ftx",
            "public_key": "public_key",
            "private_key": "*" * 10,
            "market_name_format": "market_name_format",
            "start_money": 100.0,
            "base_asset": "USDT",
            "real_time": True,
            "fee": 0.01,
            "balance_precision": 0.00001,
            "leverage": 1.0
        })
