#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import config.detector
import trader.leverage.simple
import exchange.interface
import exchange.factory


class SimpleLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"
        cls.config.trader.detectors = [
            config.detector.DetectorConfig({
                "bullish_threshold": -0.4,
                "bearish_threshold": 0.4
            })
        ]

        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(
            cls.config)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.leverage.simple.SimpleLeverageTrader(
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

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_startup_bullish(self):
        indicator_values = [-0.46, -0.45, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_hold(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bullish(self):
        indicator_values = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bearish(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.03, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_buy_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(0.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy",
                                 return_value=False):
            self.trader.perform(0.44)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.trader.perform(0.47)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_buy_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(0.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.buy",
                                 return_value=False):
            self.trader.perform(-0.44)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.trader.perform(-0.47)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_sell_failure_when_switching_to_bearish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(-0.5)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 return_value=False):
            self.trader.perform(0.44)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.trader.perform(0.47)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)

    def test_sell_failure_when_switching_to_bullish(self):
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        self.trader.perform(0.5)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        with unittest.mock.patch("exchange.ftx_mock.FtxMock.sell",
                                 return_value=False):
            self.trader.perform(-0.44)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 0.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
        self.trader.perform(-0.45)
        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)
        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 0.0)


class MultiDetectorSimpleLeverageTraderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: config.application.ApplicationConfig = config.application.ApplicationConfig({
        })
        cls.config.testing.enabled = True
        cls.config.testing.real_time = False
        cls.config.testing.start_money = 100.0
        cls.config.testing.fee = 0.0
        cls.config.exchange.name = "ftx"
        cls.config.trader.detectors = [
            config.detector.DetectorConfig({
                "bullish_threshold": -0.4,
                "bearish_threshold": 0.4
            })
        ]

        exchange.interface.Market.name_format = \
            cls.config.exchange.market_name_format
        cls.exchange = exchange.factory.ExchangeControllerFactory.create(
            cls.config)
        cls.exchange.price_mock["BTC-USDT"] = 100.0
        cls.exchange.price_mock["BEAR-USDT"] = 10.0
        cls.exchange.price_mock["BULL-USDT"] = 5.0

    def setUp(self):
        self.trader = trader.leverage.simple.SimpleLeverageTrader(
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

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)

    def test_startup_bullish(self):
        indicator_values = [-0.46, -0.45, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_hold(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.43, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bullish(self):
        indicator_values = [0.26, 0.35, 0.47, 0.03, -0.55, -0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BULL"), 20.0)

    def test_switch_to_bearish(self):
        indicator_values = [-0.26, -0.35, -0.47, -0.03, 0.55, 0.63]
        self.assertAlmostEqual(self.exchange.get_balance("USDT"), 100.0)

        for indicator_value in indicator_values:
            self.trader.perform(indicator_value)

        self.assertAlmostEqual(self.exchange.get_balance("BEAR"), 10.0)
