#!/usr/bin/python3

import unittest

import config.application
import exchange.factory
import exchange.interface


class BinanceMockTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.controller = exchange.factory.ExchangeControllerFactory.create(
            cls.config)

    def setUp(self):
        self.controller.reset()
        self.controller.price_mock["BTC-USDT"] = 100.0
        self.controller.price_mock["BEAR-USDT"] = 10.0
        self.controller.price_mock["BULL-USDT"] = 5.0

    def test_buy_bear_and_sell_on_same_price(self):
        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BEAR-USDT"), 10))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 0.0)
        self.assertEqual(balance["BEAR"], 10.0)

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BEAR-USDT"), 10))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 100.0)
        self.assertEqual(balance["BEAR"], 0.0)

    def test_buy_bear_and_bull_and_sell_on_same_price(self):
        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 50.0)
        self.assertEqual(balance["BEAR"], 5.0)

        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                2.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 40.0)
        self.assertEqual(balance["BEAR"], 5.0)
        self.assertEqual(balance["BULL"], 2.0)

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 90.0)
        self.assertEqual(balance["BEAR"], 0.0)
        self.assertEqual(balance["BULL"], 2.0)

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                2.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 100.0)
        self.assertEqual(balance["BEAR"], 0.0)
        self.assertEqual(balance["BULL"], 0.0)

    def test_buy_bear_and_bull_and_sell_on_same_price_partially(self):
        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 50.0)
        self.assertEqual(balance["BEAR"], 5.0)

        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 25.0)
        self.assertEqual(balance["BEAR"], 5.0)
        self.assertEqual(balance["BULL"], 5.0)

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 75.0)
        self.assertEqual(balance["BEAR"], 0.0)
        self.assertEqual(balance["BULL"], 5.0)

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                2.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 85.0)
        self.assertEqual(balance["BEAR"], 0.0)
        self.assertEqual(balance["BULL"], 3.0)

    def test_buy_bear_and_sell_on_higher_price(self):
        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 50.0)
        self.assertEqual(balance["BEAR"], 5.0)

        self.controller.price_mock["BEAR-USDT"] = 20.0

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BEAR-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 150.0)
        self.assertEqual(balance["BEAR"], 0.0)

    def test_buy_bull_and_sell_on_lower_price(self):
        self.assertTrue(
            self.controller.buy(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 75.0)
        self.assertEqual(balance["BULL"], 5.0)

        self.controller.price_mock["BULL-USDT"] = 1.0

        self.assertTrue(
            self.controller.sell(
                exchange.interface.Market.create_from_string("BULL-USDT"),
                5.0))
        balance = self.controller.get_balances()
        self.assertEqual(balance["USDT"], 80.0)
        self.assertEqual(balance["BULL"], 0.0)

    def test_get_money_default(self):
        self.assertEqual(self.controller.get_money("USDT"), 100.0)

    def test_get_money_without_change(self):
        self.controller.buy(
            exchange.interface.Market.create_from_string("BULL-USDT"), 2.0)
        self.controller.buy(
            exchange.interface.Market.create_from_string("BEAR-USDT"), 5.0)
        self.assertEqual(self.controller.get_money("USDT"), 100.0)

    def test_get_money_with_higher_price(self):
        self.controller.buy(
            exchange.interface.Market.create_from_string("BULL-USDT"), 2.0)
        self.controller.buy(
            exchange.interface.Market.create_from_string("BEAR-USDT"), 5.0)

        self.controller.price_mock["BULL-USDT"] = 10.0

        self.assertEqual(self.controller.get_money("USDT"), 110.0)

    def test_get_money_with_lower_price(self):
        self.controller.buy(
            exchange.interface.Market.create_from_string("BULL-USDT"), 2.0)
        self.controller.buy(
            exchange.interface.Market.create_from_string("BEAR-USDT"), 5.0)

        self.controller.price_mock["BEAR-USDT"] = 1.0

        self.assertEqual(self.controller.get_money("USDT"), 55.0)

    def test_get_price_real_time(self):
        self.controller.set_real_time(True)
        exchange.interface.Market.name_format = "{target}{base}"
        self.assertNotAlmostEqual(
            self.controller.get_price(
                exchange.interface.Market.create_from_string("ETH-BTC")), 0.0)
        self.controller.set_real_time(False)
