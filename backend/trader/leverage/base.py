#!/usr/bin/python3

import abc

import detector.common

import trader.base


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
