#!/usr/bin/python3

import abc
import logging
import typing

import config.trader
import trader.base
import detector.factory
import detector.interface
import exchange.interface

from trader.common import TraderState


class LeverageTraderBase(trader.base.TraderBase):
    def __init__(self, configuration: config.application.ApplicationConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)
        self._configuration = configuration
        self._detectors: typing.List[detector.interface.DetectorInterface] = []
        self._state: TraderState = TraderState.BASE
        self._use_stateless_detector = False

    def initialize(self):
        for detector_config in self._configuration.trader.detectors:
            self._detectors.append(
                detector.factory.DetectorFactory.create(detector_config))

    def perform(self, value: float):
        actions = []
        for next_detector in self._detectors:
            actions.append(next_detector.check(value))

        logging.debug("Detector(s) has returned %s", str(actions))
        logging.debug("Current state is %s", str(self._state))

        if detector.common.TradingAction.BULLISH_SIGNAL in actions:
            self._bullish_logic()
        elif detector.common.TradingAction.BEARISH_SIGNAL in actions:
            self._bearish_logic()

        if self._is_there_any_pending_transaction():
            self._do_pending_transaction()

        logging.debug("New state is %s", str(self._state))

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

    def _is_there_any_pending_transaction(self):
        return self._state in [
            TraderState.BUYING_BULLISH,
            TraderState.BUYING_BEARISH,
            TraderState.SELLING_BULLISH,
            TraderState.SELLING_BEARISH,
        ]

    @abc.abstractmethod
    def _bullish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_logic(self):  # pragma: no cover
        pass
