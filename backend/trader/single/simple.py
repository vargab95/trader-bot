#!/usr/bin/python3

import logging
import typing

import config.application
import exchange.interface
import detector.interface

from trader.common import TraderState
from trader.base import TraderBase


class SimpleSingleMarketTrader(TraderBase):
    def __init__(self, configuration: config.application.ApplicationConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)
        self._configuration = configuration
        self._detectors: typing.List[detector.interface.DetectorInterface] = []
        self._state: TraderState = TraderState.BASE
        self._use_stateless_detector = False

    def initialize(self):
        for threshold in self._configuration.trader.thresholds:
            self._detectors.append(
                detector.factory.DetectorFactory.create(
                    threshold["bear"], threshold["bull"],
                    self._configuration.trader.falling_edge_detection,
                    self._use_stateless_detector))
    
    def perform(self, value: float):
        actions = []
        for next_detector in self._detectors:
            actions.append(next_detector.check(value))

        logging.debug("Detector(s) has returned %s", str(actions))
        logging.debug("Current state is %s", str(self._state))

        if detector.common.TradingAction.BULLISH_SIGNAL in actions and self._state != TraderState.BULLISH:
            self._buy(self._configuration.exchange.watched_market)
            self._state = TraderState.BULLISH
        elif detector.common.TradingAction.BEARISH_SIGNAL in actions and self._state != TraderState.BASE:
            self._sell(self._configuration.exchange.watched_market)
            self._state = TraderState.BASE

        logging.debug("New state is %s", str(self._state))