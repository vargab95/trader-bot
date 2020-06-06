#!/usr/bin/python3

import abc
import typing


class Market:
    name_format = ""

    def __init__(self, base: str, target: str):
        self.base: str = base
        self.target: str = target
        self.price: float = 0.0
        self.amount: float = 0.0

    @classmethod
    def create_from_string(cls, name: str):
        name_elements = name.split("-")
        return cls(name_elements[1], name_elements[0])

    @property
    def key(self):
        return self.name_format.format(base=self.base, target=self.target)

    def __str__(self):
        return self.name_format.format(base=self.base, target=self.target)


class Balances(dict):
    def __str__(self):
        return "\nBalances:" + \
               "\n   " + \
               "\n   ".join([
                   "{}: {}".format(name, value)
                   for name, value
                   in self.items()
               ])


class ExchangeError(Exception):
    pass


class ExchangeInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def buy(self, market: Market, amount: float) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def sell(self, market: Market, amount: float) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_balances(self) -> Balances:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_balance(self, market: str) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_price(self, market: Market) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_money(self, base: str) -> float:
        pass  # pragma: no cover
