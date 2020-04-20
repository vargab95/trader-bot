#!/usr/bin/python3

import traders.leverage.base
import traders.common

from traders.common import TraderState, BuyState, SellState


class SimpleLeverageTrader(traders.leverage.base.LeverageTraderBase):
    def _bullish_logic(self):
        if self._state != TraderState.BULLISH:
            if self._state != TraderState.BASE:
                if self._sell(self._configuration.exchange.bearish_market):
                    self._state = TraderState.BUYING_BULLISH
                else:
                    self._state = TraderState.SELLING_BEARISH
            else:
                self._state = TraderState.BUYING_BULLISH
            if self._state == TraderState.BUYING_BULLISH and \
               self._buy(self._configuration.exchange.bullish_market):
                self._state = TraderState.BULLISH

    def _bearish_logic(self):
        if self._state != TraderState.BEARISH:
            if self._state != TraderState.BASE:
                if self._sell(self._configuration.exchange.bullish_market):
                    self._state = TraderState.BUYING_BEARISH
                else:
                    self._state = TraderState.SELLING_BULLISH
            else:
                self._state = TraderState.BUYING_BEARISH
            if self._state == TraderState.BUYING_BEARISH and \
               self._buy(self._configuration.exchange.bearish_market):
                self._state = TraderState.BEARISH
