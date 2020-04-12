#!/usr/bin/python3

import logging

import config.market
import traders.base
import traders.common
import exchange.interface


class SteppedLeverageTrader(traders.leverage.base.LeverageTraderBase):
    def __init__(self, configuration: config.trader.TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(used_exchange)

        # 0 is the NONE
        # 1 is one pack of bull
        # -1 is one pack of bear
        self._state = 0

        self._pack_ratio = 1.0 / configuration.market.max_steps
        self._max_steps = configuration.market.max_steps

    def _bullish_logic(self):
        if self._state < 0:
            self._sell(self._configuration.exchange.bearish_market)
            self._state = 0
        if self._state <= self._max_steps:
            if self._buy(self._configuration.exchange.bullish_market):
                self._state += 1
        else:
            logging.warning("Step limit reached %d", self._state)

    def _bearish_logic(self):
        if self._state > 0:
            self._sell(self._configuration.exchange.bullish_market)
            self._state = 0
        if self._state >= -self._max_steps:
            if self._buy(self._configuration.exchange.bearish_market):
                self._state -= 1
        else:
            logging.warning("Step limit reached %d", self._state)
