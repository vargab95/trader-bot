#!/usr/bin/python3

import abc
import typing

class Balances:
    def __init__(self):
        self.__store: typing.Dict[str, float] = {}

    def __getitem__(self, key):
        return self.__store[key]

class ExchangeInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def buy(market_name: str, amount: float) -> bool:
        pass

    @abc.abstractmethod
    def sell(market_name: str, amount: float) -> bool:
        pass

    @abc.abstractmethod
    def get_balances(self) -> Balances:
        pass

    @abc.abstractmethod
    def get_price(self, market_name: str):
        pass
