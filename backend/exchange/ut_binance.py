#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import exchange.factory
import exchange.interface


@unittest.mock.patch("exchange.binance.binance.client.Client")
class BinanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = False
        cls.config.exchange.market_name_format = "{target}{base}"
        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format

    def test_buy(self, mock_client):
        pass

    def test_sell(self, mock_client):
        pass

    def test_get_balances(self, mock_client):
        pass

    def test_get_balance(self, mock_client):
        pass
        # controller = exchange.factory.ExchangeControllerFactory.create(
        #     self.config)
        # controller.get_balance("ETH")
        # mock_client.Client.get_asset_balance.assert_called_once()

    def test_get_price(self, mock_client):
        pass

    def test_get_money(self, mock_client):
        pass
