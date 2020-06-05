#!/usr/bin/python3

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
        cls.controller = exchange.factory.ExchangeControllerFactory.create(
            cls.config)
