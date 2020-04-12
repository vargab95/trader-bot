#!/usr/bin/python3

import logging

import config.market
import traders.base
import traders.common
import detector.factory
import detector.interface
import exchange.interface


class SimpleLeverageTrader(traders.base.TraderBase):
    def __init__(self, configuration: config.trader.TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)
        self.__configuration = configuration
        self.__detector: detector.interface.DetectorInterface
        self.__state = traders.common.BuyState.NONE

    def initialize(self):
        self.__detector = detector.factory.DetectorFactory.create(
            self.__configuration.market)

    def perform(self, value: float):
        action = self.__detector.check(value)

        logging.debug("Detector has returned %s", str(action))
        logging.debug("Current state is %s", str(self.__state))

        if action == detector.common.TradingAction.SWITCH_TO_BULLISH:
            if self.__state != traders.common.BuyState.BULLISH:
                if self.__state != traders.common.BuyState.NONE:
                    self._sell(self.__configuration.exchange.bearish_market)
                if self._buy(self.__configuration.exchange.bullish_market):
                    self.__state = traders.common.BuyState.BULLISH
                else:
                    self.__state = traders.common.BuyState.SWITCHING_TO_BULLISH

        elif action == detector.common.TradingAction.SWITCH_TO_BEARISH:
            if self.__state != traders.common.BuyState.BEARISH:
                if self.__state != traders.common.BuyState.NONE:
                    self._sell(self.__configuration.exchange.bullish_market)
                if self._buy(self.__configuration.exchange.bearish_market):
                    self.__state = traders.common.BuyState.BEARISH
                else:
                    self.__state = traders.common.BuyState.SWITCHING_TO_BEARISH

        logging.debug("New state is %s", str(self.__state))
