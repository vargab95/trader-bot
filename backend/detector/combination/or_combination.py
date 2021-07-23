#!/usr/bin/python3

import typing

from detector.common import TradingAction
from detector.combination.base import DetectorCombinationLogic


class DetectorOrCombination(DetectorCombinationLogic):
    def _calculate(self, signals: typing.Dict[str, TradingAction]) -> TradingAction:
        signal_value_list = list(signals.values())
        bearish_signal_count = signal_value_list.count(TradingAction.BEARISH_SIGNAL)
        bullish_signal_count = signal_value_list.count(TradingAction.BULLISH_SIGNAL)

        if bearish_signal_count > 0 and bullish_signal_count == 0:
            return TradingAction.BEARISH_SIGNAL

        if bullish_signal_count > 0 and bearish_signal_count == 0:
            return TradingAction.BULLISH_SIGNAL

        return TradingAction.HOLD_SIGNAL
