#!/usr/bin/python3

import math

import config.exchange
import exchange.interface
import exchange.guard


class ExchangeBase(exchange.interface.ExchangeInterface):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        self._public_key = configuration.public_key
        self._private_key = configuration.private_key
        self._min_amount = dict()
        self._min_notional = dict()

    def _is_enough_amount(self, market, amount: float):
        if amount < self._min_amount[market.key]:
            return False

        price = self.get_price(market)
        if amount < (self._min_notional[market.key] / price):
            return False

        return True

    def _get_balances_in_different_base(
            self, base: str) -> exchange.interface.Balances:
        balances = exchange.interface.Balances()
        for name, balance in self.get_balances().items():
            if base == name:
                balances[name] = balance
            else:
                market = exchange.interface.Market(base, name)
                price = self.get_price(market)
                balances[name] = balance * price
        return balances

    @staticmethod
    def _floor(value: float, precision: float) -> float:
        exponent = -int(math.log10(precision))
        remainder = value % precision
        result = value
        if remainder > (0.5 * precision) and round(remainder, 12) != precision:
            result -= precision
        result = round(result, exponent)
        return abs(result)

    def get_money(self, base: str) -> float:
        all_money: float = 0.0
        for _, balance in self._get_balances_in_different_base(base).items():
            all_money += balance
        return all_money

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        pass

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        pass

    def get_balances(self) -> exchange.interface.Balances:
        pass

    def get_balance(self, market: str) -> float:
        pass

    def get_price(self, market: exchange.interface.Market) -> float:
        return -1.0
