#!/usr/bin/python3

import unittest.mock

from config.exchange import ExchangeConfig
import exchange.factory
import exchange.interface

import exchange.test_mock_common


class BinanceMockTest(exchange.test_mock_common.CommonMockTest):
    @classmethod
    @unittest.mock.patch("binance.client.Client.ping")
    @unittest.mock.patch("binance.client.Client.get_exchange_info")
    @unittest.mock.patch("binance.client.Client.get_ticker")
    def setUpClass(cls, *_):
        cls.config: ExchangeConfig = ExchangeConfig({})
        cls.config.real_time = False
        cls.config.start_money = 100.0
        cls.config.fee = 0.0
        cls.config.name = "binance"
        exchange.interface.Market.name_format = cls.config.market_name_format
        cls.controller = exchange.factory.ExchangeControllerFactory.create(cls.config, testing=True)

    @unittest.mock.patch("binance.client.Client.ping")
    @unittest.mock.patch("binance.client.Client.get_exchange_info")
    @unittest.mock.patch("binance.client.Client.get_ticker")
    def test_get_price_unsuccessful(self, get_price_mock, *_):
        get_price_mock.return_value = {}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertFalse(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")))
        self.controller.set_real_time(False)

    @unittest.mock.patch("binance.client.Client.ping")
    @unittest.mock.patch("binance.client.Client.get_exchange_info")
    @unittest.mock.patch("binance.client.Client.get_ticker")
    def test_get_price_successful(self, get_price_mock, *_):
        get_price_mock.return_value = {"lastPrice": 1.2}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertAlmostEqual(self.controller.get_price(
                exchange.interface.Market.create_from_string("BEAR-USDT")), 1.2)
        self.controller.set_real_time(False)
