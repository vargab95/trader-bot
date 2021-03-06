#!/usr/bin/python3

import unittest
import unittest.mock

import config.trader
import trader.factory
import trader.leverage.simple
import trader.leverage.stepped
import trader.single.simple
import trader.future.simple


class TraderFactoryTest(unittest.TestCase):
    def test_create_leverage_simple(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "simple"
        configuration.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertIsInstance(trader_ins, trader.leverage.simple.SimpleLeverageTrader)

    def test_create_leverage_stepped(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "stepped"
        configuration.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertIsInstance(trader_ins, trader.leverage.stepped.SteppedLeverageTrader)

    def test_create_single_stepped(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "simple"
        configuration.leverage = False
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertIsInstance(trader_ins, trader.single.simple.SimpleSingleMarketTrader)

    def test_create_future_simple(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "simple"
        configuration.leverage = False
        configuration.future = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertIsInstance(trader_ins, trader.future.simple.SimpleFutureTrader)

    def test_create_invalid(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "non-existing method"
        configuration.leverage = True
        with self.assertRaises(trader.factory.InvalidTradingMethod):
            trader.factory.TraderFactory.create(configuration, None)
