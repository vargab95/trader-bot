#!/usr/bin/python3

import typing

from config.detector import DetectorCombinationConfig

from detector.common import TradingAction
from detector.combination.base import DetectorCombinationLogic


class SwitchFirstHoldToReturnCombination(DetectorCombinationLogic):
    def __init__(self, config: DetectorCombinationConfig):
        super().__init__(config)
        self.__last_value: TradingAction = None

    def _calculate(self, signals: typing.Dict[str, TradingAction]) -> TradingAction:
        signal = list(signals.values())[0]

        checked_signals = [TradingAction.BEARISH_SIGNAL, TradingAction.BULLISH_SIGNAL]
        if signal == TradingAction.HOLD_SIGNAL and self.__last_value in checked_signals:
            result = TradingAction.RETURN_TO_BASE_SIGNAL
        else:
            result = signal

        self.__last_value = signal

        return result
