#!/usr/bin/python3

import abc
import typing
import logging

import config.application
import exchange.interface
import detector.interface
import detector.factory

from trader.common import TraderState


class TraderBase:
    def __init__(self,
                 configuration: config.application.ApplicationConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        self._exchange = used_exchange
        self._state: TraderState = TraderState.BASE
        self._configuration = configuration
        self._detectors: typing.List[detector.interface.DetectorInterface] = []
        self._use_stateless_detector = False

    @property
    def state(self):
        return self._state

    def initialize(self):
        for detector_config in self._configuration.trader.detectors:
            self._detectors.append(
                detector.factory.DetectorFactory.create(detector_config))

    def perform(self, indicator_signal: float):
        actions = []
        for next_detector in self._detectors:
            actions.append(next_detector.check(indicator_signal))

        logging.debug("Detector(s) has returned %s", str(actions))
        logging.debug("Current state is %s", str(self._state))

        if self._bullish_condition(actions):
            self._bullish_logic()
        elif self._bearish_condition(actions):
            self._bearish_logic()

        if self._is_there_any_pending_transaction():
            self._do_pending_transaction()

        logging.debug("New state is %s", str(self._state))

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

    def _is_there_any_pending_transaction(self):
        return self._state in [
            TraderState.BUYING_BULLISH,
            TraderState.BUYING_BEARISH,
            TraderState.SELLING_BULLISH,
            TraderState.SELLING_BEARISH,
        ]

    def _do_pending_transaction(self):
        if TraderState.SELLING_BULLISH == self._state:
            if self._sell(self._configuration.exchange.bullish_market):
                self._state = TraderState.BUYING_BEARISH
        if TraderState.SELLING_BEARISH == self._state:
            if self._sell(self._configuration.exchange.bearish_market):
                self._state = TraderState.BUYING_BULLISH
        if TraderState.BUYING_BEARISH == self._state:
            if self._buy(self._configuration.exchange.bearish_market):
                self._state = TraderState.BEARISH
        if TraderState.BUYING_BULLISH == self._state:
            if self._buy(self._configuration.exchange.bullish_market):
                self._state = TraderState.BULLISH

    @abc.abstractmethod
    def _bullish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bullish_condition(self, actions: typing.List[detector.common.TradingAction]):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_condition(self, actions: typing.List[detector.common.TradingAction]):  # pragma: no cover
        pass
