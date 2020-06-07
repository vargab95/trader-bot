#!/usr/bin/python3

import abc

import exchange.interface
from trader.common import TraderState


class TraderBase:
    def __init__(self, used_exchange: exchange.interface.ExchangeInterface):
        self._exchange = used_exchange
        self._state: TraderState

    @property
    def state(self):
        return self._state

    @abc.abstractmethod
    def initialize(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def perform(self, value: float):
        pass  # pragma: no cover

    def _sell(self,
              market: exchange.interface.Market,
              ratio: float = 1.0) -> bool:
        amount = self._exchange.get_balance(market.target) * ratio
        return self._exchange.sell(market, amount)

    def _buy(self,
             market: exchange.interface.Market,
             ratio: float = 1.0) -> bool:
        balance = self._exchange.get_balance(market.base)
        price = self._exchange.get_price(market)
        amount = balance / price * ratio
        return self._exchange.buy(market, amount)
