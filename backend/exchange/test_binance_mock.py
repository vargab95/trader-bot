#!/usr/bin/python3

import unittest.mock

import config.application
import exchange.factory
import exchange.interface

import exchange.test_mock_common


class BinanceMockTest(exchange.test_mock_common.CommonMockTest):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "binance"
        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        # TODO with unittest.mock.patch("exchange.binance.binance.client.Client"):
        cls.controller = exchange.factory.ExchangeControllerFactory.create(
            cls.config)

    @unittest.mock.patch("binance.client.Client.get_ticker")
    def test_get_price_unsuccessful(self, get_price_mock):
        get_price_mock.return_value = {}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertFalse(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")))
        self.controller.set_real_time(False)

    @unittest.mock.patch("binance.client.Client.get_ticker")
    def test_get_price_successful(self, get_price_mock):
        get_price_mock.return_value = {"lastPrice": 1.2}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertAlmostEqual(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")), 1.2)
        self.controller.set_real_time(False)
