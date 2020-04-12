#!/usr/bin/python3

import traders.leverage.base
import traders.common


class SimpleLeverageTrader(traders.leverage.base.LeverageTraderBase):
    def _bullish_logic(self):
        if self._state != traders.common.BuyState.BULLISH:
            if self._state != traders.common.BuyState.NONE:
                self._sell(self._configuration.exchange.bearish_market)
            if self._buy(self._configuration.exchange.bullish_market):
                self._state = traders.common.BuyState.BULLISH
            else:
                self._state = traders.common.BuyState.SWITCHING_TO_BULLISH

    def _bearish_logic(self):
        if self._state != traders.common.BuyState.BEARISH:
            if self._state != traders.common.BuyState.NONE:
                self._sell(self._configuration.exchange.bullish_market)
            if self._buy(self._configuration.exchange.bearish_market):
                self._state = traders.common.BuyState.BEARISH
            else:
                self._state = traders.common.BuyState.SWITCHING_TO_BEARISH
