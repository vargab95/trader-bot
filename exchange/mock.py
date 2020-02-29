#!/usr/bin/python3

import exchange.interface

class BinanceMock(exchange.interface.ExchangeInterface):
    def __init__(self, start_money):
        self.current_money = start_money

    def buy(market_name: str, amount: float) -> bool:
        pass

    def sell(market_name: str, amount: float) -> bool:
        pass

    def get_balances(self) -> exchange.interface.Balances:
        pass

    def get_price(self, market_name: str):
        pass
