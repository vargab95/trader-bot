#!/usr/bin/python3

import detector.interface

from trader.common import TraderState
from trader.base import TraderBase


class SimpleSingleMarketTrader(TraderBase):
    def _bullish_logic(self):
        if self._buy(self._configuration.market):
            self._state = TraderState.BULLISH
        else:
            self._state = TraderState.BUYING_BULLISH

    def _bearish_logic(self):
        if self._sell(self._configuration.market):
            self._state = TraderState.BASE
        else:
            self._state = TraderState.SELLING_BULLISH

    def _bullish_condition(self, action: detector.common.TradingAction):
        return self._state == TraderState.BUYING_BULLISH or \
            (detector.common.TradingAction.BULLISH_SIGNAL == action and self._state != TraderState.BULLISH)

    def _bearish_condition(self, action: detector.common.TradingAction):
        return self._state == TraderState.SELLING_BULLISH or \
            (detector.common.TradingAction.BEARISH_SIGNAL == action and self._state != TraderState.BASE)
