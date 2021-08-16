#!/usr/bin/python3

import trader.future.base
import trader.common

from trader.common import TraderState


class SimpleFutureTrader(trader.future.base.FutureTraderBase):
    def _bullish_logic(self):
        if self._state != TraderState.BULLISH:
            if self._state != TraderState.BASE:
                if self._sell(self._configuration.market):
                    self._state = TraderState.BUYING_BULLISH
                else:
                    self._state = TraderState.SELLING_BEARISH
            else:
                self._state = TraderState.BUYING_BULLISH
            if self._state == TraderState.BUYING_BULLISH and \
               self._buy(self._configuration.market):
                self._state = TraderState.BULLISH

    def _bearish_logic(self):
        if self._state != TraderState.BEARISH:
            if self._state != TraderState.BASE:
                if self._sell(self._configuration.market):
                    self._state = TraderState.BUYING_BEARISH
                else:
                    self._state = TraderState.SELLING_BULLISH
            else:
                self._state = TraderState.BUYING_BEARISH
            if self._state == TraderState.BUYING_BEARISH and \
               self._buy(self._configuration.market):
                self._state = TraderState.BEARISH

    def _return_to_base_logic(self):
        if self._state == TraderState.BULLISH:
            if self._sell(self._configuration.market):
                self._state = TraderState.BASE
            else:
                self._state = TraderState.SELLING_BULLISH
        elif self._state == TraderState.BEARISH:
            if self._sell(self._configuration.market):
                self._state = TraderState.BASE
            else:
                self._state = TraderState.SELLING_BEARISH
