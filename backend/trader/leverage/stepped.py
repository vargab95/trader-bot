#!/usr/bin/python3

import logging

import config.trader
import trader.base
import trader.common
import trader.leverage.base
import exchange.interface


class SteppedLeverageTrader(trader.leverage.base.LeverageTraderBase):
    def __init__(self, configuration: config.trader.TraderConfig,
                 used_exchange: exchange.interface.ExchangeInterface):
        super().__init__(configuration, used_exchange)

        # 0 is the NONE
        # 1 is one pack of bull
        # -1 is one pack of bear
        self._state = 0

        self._pack_ratio = 1.0 / configuration.max_steps
        self._max_steps = configuration.max_steps
        self._use_stateless_detector = True

    def _bullish_logic(self):
        if self._state < 0:
            self._sell(self._configuration.bearish_market)
            self._state = 0
            self._pack_ratio = 1.0 / self._configuration.max_steps
        if self._state < self._max_steps:
            # FIXME That state is not handled properly, when this buy statement
            # fails, because it won't take into account the bullish signal
            # anymore
            # TODO Unittests should be written for this behaviour here and also
            # for the bearish case
            self._buy(self._configuration.bullish_market, self._pack_ratio)
            self._state += 1
            if self._state != self._configuration.max_steps:
                self._pack_ratio = 1.0 / (self._configuration.max_steps - self._state)
        else:
            logging.warning("Step limit reached %d", self._state)

    def _bearish_logic(self):
        if self._state > 0:
            self._sell(self._configuration.bullish_market)
            self._state = 0
            self._pack_ratio = 1.0 / self._configuration.max_steps
        if self._state > -self._max_steps:
            self._buy(self._configuration.bearish_market, self._pack_ratio)
            self._state -= 1
            # FIXME a better solution may be found
            if self._state * -1 != self._configuration.max_steps:
                self._pack_ratio = 1.0 / (self._configuration.max_steps + self._state)
        else:
            logging.warning("Step limit reached %d", self._state)

    def _return_to_base_logic(self):
        if self._state != 0:
            if self._state < 0:
                self._sell(self._configuration.bearish_market)
            elif self._state > 0:
                self._sell(self._configuration.bullish_market)
            self._state = 0
            self._pack_ratio = 1.0 / self._configuration.max_steps

    def _detect_and_set_start_state(self):
        raise NotImplementedError("Auto detecting start state is currently not implemented for stepped variant")
