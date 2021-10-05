#!/usr/bin/python3

from exchange.interface import ExchangeError
import detector.interface

from trader.common import TraderState
from trader.base import TraderBase


class SimpleSingleMarketTrader(TraderBase):
    def _bullish_logic(self):
        try:
            self._buy(self._configuration.market)
            self._state = TraderState.BULLISH
        except ExchangeError:
            self._state = TraderState.BUYING_BULLISH
            raise

    def _bearish_logic(self):
        try:
            self._sell(self._configuration.market)
            self._state = TraderState.BASE
        except ExchangeError:
            self._state = TraderState.SELLING_BULLISH
            raise

    def _return_to_base_logic(self):
        self._bearish_logic()

    def _bullish_condition(self, action: detector.common.TradingAction):
        return self._state == TraderState.BUYING_BULLISH or \
            (detector.common.TradingAction.BULLISH_SIGNAL == action and self._state != TraderState.BULLISH)

    def _bearish_condition(self, action: detector.common.TradingAction):
        return self._state == TraderState.SELLING_BULLISH or \
            (detector.common.TradingAction.BEARISH_SIGNAL == action and self._state != TraderState.BASE)

    def _detect_and_set_start_state(self):
        if self._exchange.get_balance(self._configuration.market.target) > 0:
            self._state = TraderState.BULLISH
        else:
            self._state = TraderState.BASE
