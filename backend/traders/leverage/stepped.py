#!/usr/bin/python3

import logging

import config.trader
import traders.base
import traders.common
import traders.leverage.base
import exchange.interface


class SteppedLeverageTrader(traders.leverage.base.LeverageTraderBase):
    def __init__(self, configuration: config.application.ApplicationConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(configuration, used_exchange)

        # 0 is the NONE
        # 1 is one pack of bull
        # -1 is one pack of bear
        self._state = 0

        self._pack_ratio = 1.0 / configuration.trader.max_steps
        self._max_steps = configuration.trader.max_steps
        self._use_stateless_detector = True

    def _bullish_logic(self):
        if self._state < 0:
            self._sell(self._configuration.exchange.bearish_market)
            self._state = 0
            self._pack_ratio = 1.0 / self._configuration.trader.max_steps
        if self._state < self._max_steps:
            # FIXME That state is not handled properly, when this buy statement
            # fails, because it won't take into account the bullish signal
            # anymore
            # TODO Unittests should be written for this behaviour here and also
            # for the bearish case
            if self._buy(self._configuration.exchange.bullish_market,
                         self._pack_ratio):
                self._state += 1
                if self._state != self._configuration.trader.max_steps:
                    self._pack_ratio = 1.0 / (
                        self._configuration.trader.max_steps - self._state)
        else:
            logging.warning("Step limit reached %d", self._state)

    def _bearish_logic(self):
        if self._state > 0:
            self._sell(self._configuration.exchange.bullish_market)
            self._state = 0
            self._pack_ratio = 1.0 / self._configuration.trader.max_steps
        if self._state > -self._max_steps:
            if self._buy(self._configuration.exchange.bearish_market,
                         self._pack_ratio):
                self._state -= 1
                # FIXME a better solution may be found
                if self._state * -1 != self._configuration.trader.max_steps:
                    self._pack_ratio = 1.0 / (
                        self._configuration.trader.max_steps + self._state)
        else:
            logging.warning("Step limit reached %d", self._state)
