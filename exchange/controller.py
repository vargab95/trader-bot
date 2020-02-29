#!/usr/bin/python3

import binance.client

import config
import exchange.interface

class BinanceController(exchange.interface.ExchangeInterface):
    def __init__(self, config: config.ExchangeConfig):
        self.client = binance.client.Client(config.public_key, config.private_key)

    def buy(market_name: str, amount: float) -> bool:
        pass

    def sell(market_name: str, amount: float) -> bool:
        pass

    def get_balances(self) -> exchange.interface.Balances:
        pass

    def get_price(self, market_name: str) -> float:
        return float(self.client.get_ticker(symbol="BTCUSDT")["lastPrice"])
