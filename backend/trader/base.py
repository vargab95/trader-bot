#!/usr/bin/python3

import abc
import logging

import config.application
import exchange.interface
import detector.interface
import detector.factory
from detector.common import TradingAction

from trader.common import TraderState


class TraderBase:
    def __init__(self,
                 configuration: config.application.ApplicationConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        self._exchange = used_exchange
        self._state: TraderState = configuration.start_state
        self._configuration = configuration
        self._use_stateless_detector = False

    @property
    def state(self):  # pragma: no cover
        return self._state

    def perform(self, action: TradingAction):

        logging.debug("Detector(s) has returned %s", str(action))
        logging.debug("Current state is %s", str(self._state))

        if self._bullish_condition(action):
            self._bullish_logic()
        elif self._bearish_condition(action):
            self._bearish_logic()
        elif self._return_to_base_condition(action):
            self._return_to_base_logic()

        logging.debug("New state is %s", str(self._state))

    def _sell(self,
              market: exchange.interface.Market,
              ratio: float = 1.0) -> bool:
        amount = self._exchange.get_balance(market.target) * ratio
        return self._exchange.sell(market, amount)

    def _buy(self,
             market: exchange.interface.Market,
             ratio: float = 1.0) -> bool:
        for _ in range(5):
            balance = self._exchange.get_balance(market.base)
            price = self._exchange.get_price(market, future=self._configuration.future)
            amount = balance / price * ratio
            if self._exchange.buy(market, amount):
                return True
            ratio *= 0.99
        return False

    @abc.abstractmethod
    def _bullish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _return_to_base_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bullish_condition(self, action: detector.common.TradingAction):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_condition(self, action: detector.common.TradingAction):  # pragma: no cover
        pass

    def _return_to_base_condition(self, action: detector.common.TradingAction):
        return action == TradingAction.RETURN_TO_BASE_SIGNAL and self.state != TraderState.BASE
