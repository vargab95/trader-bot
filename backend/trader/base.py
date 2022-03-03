#!/usr/bin/python3

import abc
import logging

from config.trader import TraderConfig
import exchange.interface
import detector.interface
import detector.factory
from detector.common import TradingAction

from trader.common import TraderState


class TraderBase:
    def __init__(self,
                 configuration: TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        self._exchange = used_exchange
        self._state: TraderState = configuration.start_state if not configuration.auto_detect_start_state else None
        self._configuration = configuration
        self._use_stateless_detector = False
        self.__first_run = True

    @property
    def state(self):  # pragma: no cover
        return self._state

    def perform(self, action: TradingAction):
        logging.debug("Detector(s) has returned %s", str(action))

        if self.__first_run and self._configuration.auto_detect_start_state:
            self._detect_and_set_start_state()
            self.__first_run = False

            logging.info("Auto detected starting state: %s", str(self.state))

        logging.debug("Current state is %s", str(self._state))

        if self._bullish_condition(action):
            self._bullish_logic()
        elif self._bearish_condition(action):
            self._bearish_logic()
        elif self._return_to_base_condition(action):
            self._return_to_base_logic()
        elif self._is_there_any_pending_transaction():
            self._do_pending_transaction()

        logging.debug("New state is %s", str(self._state))

    @abc.abstractmethod
    def _detect_and_set_start_state(self):
        pass  # pragma: no cover

    def _sell(self,
              market: exchange.interface.Market,
              ratio: float = 1.0) -> None:
        amount = self._exchange.get_balance(market.target) * ratio
        self._exchange.sell(market, amount)

    def _buy(self,
             market: exchange.interface.Market,
             ratio: float = 1.0) -> None:
        last_exception = None
        for _ in range(5):
            balance = self._exchange.get_balance(market.base)
            price = self._exchange.get_price(market, future=self._configuration.future)
            amount = balance / price * ratio
            try:
                self._exchange.buy(market, amount)
                return
            except exchange.interface.InsufficientFundsError as exc:
                ratio *= 0.99
                last_exception = exc
        raise last_exception

    def _is_there_any_pending_transaction(self):
        return self._state in [
            TraderState.BUYING_BULLISH,
            TraderState.BUYING_BEARISH,
            TraderState.SELLING_BULLISH,
            TraderState.SELLING_BEARISH,
        ]

    def _do_pending_transaction(self):
        if TraderState.SELLING_BULLISH == self._state:
            self._sell(self._configuration.bullish_market)
            self._state = TraderState.BUYING_BEARISH
        if TraderState.SELLING_BEARISH == self._state:
            self._sell(self._configuration.bearish_market)
            self._state = TraderState.BUYING_BULLISH
        if TraderState.BUYING_BEARISH == self._state:
            self._buy(self._configuration.bearish_market)
            self._state = TraderState.BEARISH
        if TraderState.BUYING_BULLISH == self._state:
            self._buy(self._configuration.bullish_market)
            self._state = TraderState.BULLISH

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
