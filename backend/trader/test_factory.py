#!/usr/bin/python3

import unittest
import unittest.mock

import config.trader
import trader.factory
import trader.leverage.simple
import trader.leverage.stepped
import trader.single.simple


class TraderFactoryTest(unittest.TestCase):
    def test_create_leverage_simple(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "simple"
        configuration.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(isinstance(trader_ins, trader.leverage.simple.SimpleLeverageTrader))

    def test_create_leverage_stepped(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "stepped"
        configuration.leverage = True
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(isinstance(trader_ins, trader.leverage.stepped.SteppedLeverageTrader))

    def test_create_single_stepped(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "simple"
        configuration.leverage = False
        trader_ins = trader.factory.TraderFactory.create(configuration, None)
        self.assertTrue(isinstance(trader_ins, trader.single.simple.SimpleSingleMarketTrader))

    def test_create_invalid(self):
        configuration = config.trader.TraderConfig({})
        configuration.method = "non-existing method"
        configuration.leverage = True
        try:
            trader.factory.TraderFactory.create(configuration, None)
            self.fail()
        except trader.factory.InvalidTradingMethod:
            pass
