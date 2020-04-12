#!/usr/bin/python3

import abc
import logging

import config.market
import traders.base
import traders.common
import detector.factory
import detector.interface
import exchange.interface


class LeverageTraderBase(traders.base.TraderBase):
    def __init__(self, configuration: config.trader.TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)
        self._configuration = configuration
        self._detector: detector.interface.DetectorInterface
        self._state = traders.common.BuyState.NONE

    def initialize(self):
        self._detector = detector.factory.DetectorFactory.create(
            self._configuration.market)

    def perform(self, value: float):
        action = self._detector.check(value)

        logging.debug("Detector has returned %s", str(action))
        logging.debug("Current state is %s", str(self._state))

        if action == detector.common.TradingAction.SWITCH_TO_BULLISH:
            self._bullish_logic()
        elif action == detector.common.TradingAction.SWITCH_TO_BEARISH:
            self._bearish_logic()

        logging.debug("New state is %s", str(self._state))

    @abc.abstractmethod
    def _bullish_logic(self):
        pass

    @abc.abstractmethod
    def _bearish_logic(self):
        pass
