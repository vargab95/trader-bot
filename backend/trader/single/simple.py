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
        # TODO Refactor to have a sell and buy value instead of bear and bull
        for detector_config in self._configuration.trader.detectors:
            self._detectors.append(
                detector.factory.DetectorFactory.create(detector_config))

    def perform(self, value: float):
        actions = []
        for next_detector in self._detectors:
            actions.append(next_detector.check(value))

        logging.debug("Detector(s) has returned %s", str(actions))
        logging.debug("Current state is %s", str(self._state))

        if self._state == TraderState.BUYING_BULLISH or \
                (detector.common.TradingAction.BULLISH_SIGNAL in actions and self._state != TraderState.BULLISH):
            if self._buy(self._configuration.exchange.watched_market):
                self._state = TraderState.BULLISH
            else:
                self._state = TraderState.BUYING_BULLISH
        elif self._state == TraderState.SELLING_BULLISH or \
                (detector.common.TradingAction.BEARISH_SIGNAL in actions and self._state != TraderState.BASE):
            if self._sell(self._configuration.exchange.watched_market):
                self._state = TraderState.BASE
            else:
                self._state = TraderState.SELLING_BULLISH

        logging.debug("New state is %s", str(self._state))
