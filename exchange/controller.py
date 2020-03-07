#!/usr/bin/python3

import binance.client

import config.exchange
import exchange.interface


class BinanceController(exchange.interface.ExchangeInterface):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        self.client = binance.client.Client(configuration.public_key,
                                            configuration.private_key)

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        pass

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        pass

    def get_balances(self) -> exchange.interface.Balances:
        pass

    def get_balance(self, balance: str) -> float:
        pass

    def get_price(self, market: exchange.interface.Market) -> float:
        return float(self.client.get_ticker(symbol=market.key)["lastPrice"])

    def get_money(self, base: str) -> float:
        pass
