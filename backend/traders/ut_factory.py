#!/usr/bin/python3

import unittest
import unittest.mock

import config.application
import traders.factory
import traders.leverage.simple
import traders.leverage.stepped


class TraderFactoryTest(unittest.TestCase):
    def test_create_simple(self):
        configuration = config.application.ApplicationConfig({})
        configuration.market.method = "simple"
        trader = traders.factory.TraderFactory.create(configuration, None)
        self.assertTrue(
            isinstance(trader, traders.leverage.simple.SimpleLeverageTrader))

    def test_create_stepped(self):
        configuration = config.application.ApplicationConfig({})
        configuration.market.method = "stepped"
        trader = traders.factory.TraderFactory.create(configuration, None)
        self.assertTrue(
            isinstance(trader, traders.leverage.stepped.SteppedLeverageTrader))

    def test_create_invalid(self):
        configuration = config.application.ApplicationConfig({})
        configuration.market.method = "non-existing method"
        try:
            traders.factory.TraderFactory.create(configuration, None)
            self.fail()
        except traders.factory.InvalidTradingMethod:
            pass
