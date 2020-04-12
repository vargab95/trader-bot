#!/usr/bin/python3

import logging

import config.market
import traders.base
import traders.common
import detector.factory
import detector.interface
import exchange.interface


class SteppedLeverageTrader(traders.base.TraderBase):
    def __init__(self, configuration: config.trader.TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)
        self.__configuration = configuration
        self.__detector: detector.interface.DetectorInterface

        # 0 is the NONE
        # 1 is one pack of bull
        # -1 is one pack of bear
        self.__state = 0

        self.__pack_ratio = 1.0 / configuration.market.max_steps
        self.__max_steps = configuration.market.max_steps

    def initialize(self):
        self.__detector = detector.factory.DetectorFactory.create(
            self.__configuration.market)

    def perform(self, value: float):
        action = self.__detector.check(value)

        logging.debug("Detector has returned %s", str(action))
        logging.debug("Current state is %s", str(self.__state))

        if action == detector.common.TradingAction.SWITCH_TO_BULLISH:
            if self.__state < 0:
                self._sell(self.__configuration.exchange.bearish_market)
                self.__state = 0
            if self.__state <= self.__max_steps:
                if self._buy(self.__configuration.exchange.bullish_market):
                    self.__state += 1
            else:
                logging.warning("Step limit reached %d", self.__state)

        elif action == detector.common.TradingAction.SWITCH_TO_BEARISH:
            if self.__state > 0:
                self._sell(self.__configuration.exchange.bullish_market)
                self.__state = 0
            if self.__state >= -self.__max_steps:
                if self._buy(self.__configuration.exchange.bearish_market):
                    self.__state -= 1
            else:
                logging.warning("Step limit reached %d", self.__state)

        logging.debug("New state is %s", str(self.__state))
