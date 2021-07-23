#!/usr/bin/python3

import typing

from detector.common import TradingAction
from detector.combination.base import DetectorCombinationLogic


class DetectorNotCombination(DetectorCombinationLogic):
    def _calculate(self, signals: typing.Dict[str, TradingAction]) -> TradingAction:
        if all(signal == TradingAction.BEARISH_SIGNAL for signal in signals.values()):
            return TradingAction.BULLISH_SIGNAL

        if all(signal == TradingAction.BULLISH_SIGNAL for signal in signals.values()):
            return TradingAction.BEARISH_SIGNAL

        return TradingAction.HOLD_SIGNAL
