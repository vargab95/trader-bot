#!/usr/bin/python3

import abc
import math

from signals.trading_signal import TradingSignal, TickerSignalDescriptor


class Market:
    def __init__(self, base: str, target: str):
        self.base: str = base
        self.target: str = target
        self.price: float = 0.0
        self.amount: float = 0.0

    @classmethod
    def create_from_string(cls, name: str):
        name_elements = name.split("-")
        return cls(name_elements[1], name_elements[0])

    def key(self, name_format="{target}-{base}"):
        return name_format.format(base=self.base, target=self.target)

    def __str__(self):
        return f"{self.target}-{self.base}"

    def __repr__(self):
        return str(self)


class Balances(dict):
    def __str__(self):
        return "\nBalances:" + \
               "\n   " + \
               "\n   ".join([
                   "{}: {}".format(name, value)
                   for name, value
                   in self.items()
               ])

    def copy(self) -> "Balances":
        return Balances(super().copy())


class ExchangeError(Exception):
    pass


class ZeroOrNegativeAmountError(ExchangeError):
    pass


class InsufficientFundsError(ExchangeError):
    pass


class UnknownProviderExchangeError(ExchangeError):
    pass


class PositionLiquidatedError(ExchangeError):
    pass


class ExchangeInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bet_on_bearish(self, market: Market, amount: float):
        pass  # pragma: no cover

    @abc.abstractmethod
    def bet_on_bullish(self, market: Market, amount: float):
        pass  # pragma: no cover

    def close_position(self, market: Market):
        position = self.get_position(market)
        if position < 0:
            self.bet_on_bullish(market, -position)
        elif position > 0:
            self.bet_on_bearish(market, position)
        else:
            raise ZeroOrNegativeAmountError("Cannot close position with 0 value")

    @abc.abstractmethod
    def buy(self, market: Market, amount: float) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def sell(self, market: Market, amount: float) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_balances(self) -> Balances:
        pass  # pragma: no cover

    @property
    def balances(self) -> Balances:
        return self.get_balances()

    @abc.abstractmethod
    def get_balance(self, market: str) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_leverage_balance(self) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_price(self, market: Market, keyword: str = "", future: bool = False) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_price_history(self, descriptor: TickerSignalDescriptor) -> TradingSignal:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_money(self, base: str | None = None) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_positions(self) -> Balances:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_future_loans(self) -> Balances:
        pass  # pragma: no cover

    @property
    def positions(self) -> Balances:
        return self.get_positions()

    @abc.abstractmethod
    def get_position(self, market: Market) -> float:
        pass  # pragma: no cover

    @staticmethod
    def floor(value: float, precision: float) -> float:
        sign = -1 if value < 0 else 1
        exponent = -int(math.log10(precision))
        result = abs(value)
        remainder = result % precision
        if abs(remainder) > (0.5 * precision) and round(remainder, 12) != precision:
            result -= precision
        result = abs(result) * sign
        result = round(result, exponent)
        return result
