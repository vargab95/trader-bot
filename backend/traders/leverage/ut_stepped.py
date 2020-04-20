#!/usr/bin/python3

import unittest
import unittest.mock

import config.trader
import traders.leverage.stepped
import exchange.interface
import exchange.factory


class SteppedLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.trader.TraderConfig = config.trader.TraderConfig({})
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"
        cls.config.market.thresholds = [{"bull": -0.4, "bear": 0.4}]
        cls.config.market.max_steps = 10

        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(
            cls.config)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = traders.leverage.stepped.SteppedLeverageTrader(
            self.config, self.exchange)
        self.trader.initialize()

    def tearDown(self):
        self.exchange.reset()

    def test_startup_hold(self):
        indicator_values = [0.1, 0.05, 0.03, 0.0, 0.03, 0.01, 0.03]

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_startup_bearish(self):
        indicator_values = [0.46, 0.45, 0.47, 0.43, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 1.0)

    def test_startup_bullish(self):
        indicator_values = [-0.46, -0.45, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_hold(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.43, -0.45, -0.43]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_switches_to_bullish(self):
        indicator_values = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_switches_to_bearish(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.03, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 1.0)

    def test_exceeds_bullish(self):
        indicator_values = [
            -0.44, -0.55, -0.63, -0.44, -0.55, -0.63, -0.44, -0.55, -0.63,
            -0.44, -0.55, -0.63
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_exceeds_bearish(self):
        indicator_values = [
            0.44, 0.55, 0.63, 0.44, 0.55, 0.63, 0.44, 0.55, 0.63, 0.44, 0.55,
            0.63
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)


class MultiDetectorSteppedLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.trader.TraderConfig = config.trader.TraderConfig({})
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"
        cls.config.market.bullish_threshold = [-0.4, -0.5, -0.6]
        cls.config.market.bearish_threshold = [0.4, 0.5, 0.6]
        cls.config.market.thresholds = [{
            "bull": -0.4,
            "bear": 0.4
        }, {
            "bull": -0.5,
            "bear": 0.5
        }, {
            "bull": -0.6,
            "bear": 0.6
        }]
        cls.config.market.max_steps = 10

        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(
            cls.config)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = traders.leverage.stepped.SteppedLeverageTrader(
            self.config, self.exchange)
        self.trader.initialize()

    def tearDown(self):
        self.exchange.reset()

    def test_startup_hold(self):
        indicator_values = [0.1, 0.05, 0.03, 0.0, 0.03, 0.01, 0.03]

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

    def test_startup_bearish(self):
        indicator_values = [0.46, 0.45, 0.47, 0.43, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 3.0)

    def test_startup_bullish(self):
        indicator_values = [-0.46, -0.45, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 6.0)

    def test_hold(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.43, -0.45, -0.43]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 2.0)

    def test_switches_to_bullish(self):
        indicator_values = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 4.0)

    def test_switches_to_bearish(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.03, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 2.0)

    def test_exceeds_bullish(self):
        indicator_values = [
            -0.44, -0.55, -0.63, -0.44, -0.55, -0.63, -0.44, -0.55, -0.63,
            -0.44, -0.55, -0.63
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_exceeds_bearish(self):
        indicator_values = [
            0.44, 0.55, 0.63, 0.44, 0.55, 0.63, 0.44, 0.55, 0.63, 0.44, 0.55,
            0.63
        ]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
