#!/usr/bin/python3

import unittest.mock

from config.exchange import ExchangeConfig
import exchange.factory
import exchange.interface
from exchange.interface import Market

import exchange.test_mock_common


class FtxMockTest(exchange.test_mock_common.CommonMockTest):
    @classmethod
    def setUpClass(cls):
        cls.config: ExchangeConfig = ExchangeConfig({})
        cls.config.real_time = False
        cls.config.start_money = 100.0
        cls.config.fee = 0.0
        cls.config.name = "ftx"
        cls.controller = exchange.factory.ExchangeControllerFactory.create(cls.config, testing=True)

    @unittest.mock.patch("requests.get")
    def test_get_price_unsuccessful(self, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {}

        self.controller.set_real_time(True)
        with unittest.mock.patch("time.sleep"):
            self.assertFalse(self.controller.get_price(exchange.interface.Market.create_from_string("BEAR-USDT")))
        self.controller.set_real_time(False)

    @unittest.mock.patch("requests.get")
    def test_get_price_successful(self, get_mock):
        get_mock.return_value = unittest.mock.Mock()
        get_mock.return_value.json.return_value = {
            "success": True,
            "result": [
                {
                    "name": "BEAR/USDT",
                    "minProvideSize": 0.0,
                    "priceIncrement": 0.0,
                }
            ]
        }

        self.controller.set_real_time(True)

        get_mock.return_value.json.return_value = {
            "success": True,
            "result": {
                "last": 1.3,
                "price": 1.2
            }
        }
        with unittest.mock.patch("time.sleep"):
            self.assertAlmostEqual(self.controller.get_price(Market.create_from_string("BEAR-USDT")), 1.2)
        self.controller.set_real_time(False)


if __name__ == "__main__":
    unittest.main()
