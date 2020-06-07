#!/usr/bin/python3

import unittest

from exchange.interface import Market
from exchange.mock_base import Trade, InvalidTradeResultRequestException


class TradeTest(unittest.TestCase):
    def test_profit(self):
        trade = Trade(Market("Base", "Target"))
        trade.enter(1, 1)
        trade.finish(2)
        self.assertAlmostEqual(trade.profit, 100.0)

    def test_profit_fail(self):
        trade = Trade(Market("Base", "Target"))
        trade.enter(1, 1)
        try:
            print(trade.profit)
            self.fail()
        except InvalidTradeResultRequestException:
            pass
