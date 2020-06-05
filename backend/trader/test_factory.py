#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import trader.factory
import trader.leverage.simple
import trader.leverage.stepped
import trader.single.simple


class TraderFactoryTest(unittest.TestCase):
    def test_create_leverage_simple(self):
        configuration = config.application.ApplicationConfig({})
        configuration.trader.method = "simple"
        configuration.trader.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(
            isinstance(trader_ins, trader.leverage.simple.SimpleLeverageTrader))

    def test_create_leverage_stepped(self):
        configuration = config.application.ApplicationConfig({})
        configuration.trader.method = "stepped"
        configuration.trader.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(
            isinstance(trader_ins, trader.leverage.stepped.SteppedLeverageTrader))

    def test_create_single_stepped(self):
        configuration = config.application.ApplicationConfig({})
        configuration.trader.method = "simple"
        configuration.trader.leverage = False
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(
            isinstance(trader_ins, trader.single.simple.SimpleSingleMarketTrader))

    def test_create_invalid(self):
        configuration = config.application.ApplicationConfig({})
        configuration.trader.method = "non-existing method"
        configuration.trader.leverage = True
        try:
            trader.factory.TraderFactory.create(configuration, None)
            self.fail()
        except trader.factory.InvalidTradingMethod:
            pass
