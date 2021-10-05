#!/usr/bin/python3

import abc

import detector.common

import trader.base
from trader.common import TraderState


class LeverageTraderBase(trader.base.TraderBase):
    @abc.abstractmethod
    def _bullish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_logic(self):  # pragma: no cover
        pass

    def _bullish_condition(self, action: detector.common.TradingAction):
        return detector.common.TradingAction.BULLISH_SIGNAL == action

    def _bearish_condition(self, action: detector.common.TradingAction):
        return detector.common.TradingAction.BEARISH_SIGNAL == action

    def _detect_and_set_start_state(self):
        if self._exchange.get_balance(self._configuration.bullish_market.target) > 0:
            self._state = TraderState.BULLISH
        elif self._exchange.get_balance(self._configuration.bearish_market.target) > 0:
            self._state = TraderState.BEARISH
        else:
            self._state = TraderState.BASE
