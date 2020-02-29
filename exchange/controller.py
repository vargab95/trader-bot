#!/usr/bin/python3

import exchange.interface

class BinanceController(exchange.interface.ExchangeInterface):
    def buy(market_name: str, amount: float) -> bool:
        pass

    def sell(market_name: str, amount: float) -> bool:
        pass

    def get_balances(self) -> exchange.interface.Balances:
        pass

    def get_price(self, market_name: str):
        pass
