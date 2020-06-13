#!/usr/bin/python3

import unittest.mock

import config.application
import exchange.factory
import exchange.interface

import exchange.test_mock_common


class FtxMockTest(exchange.test_mock_common.CommonMockTest):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"
        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.controller = exchange.factory.ExchangeControllerFactory.create(
            cls.config)

    @unittest.mock.patch("requests.get")
    def test_get_price_unsuccessful(self, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertFalse(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")))
        self.controller.set_real_time(False)

    @unittest.mock.patch("requests.get")
    def test_get_price_successful(self, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertAlmostEqual(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")), 1.2)
        self.controller.set_real_time(False)
