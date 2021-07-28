#!/usr/bin/python3

import abc
import typing

from config.detector import DetectorCombinationConfig

from detector.common import TradingAction


class DetectorCombinationLogic:
    def __init__(self, config: DetectorCombinationConfig):
        self.__config = config
        self.__last_signals: typing.Dict[str, TradingAction] = dict()
        self.__result: TradingAction = TradingAction.HOLD_SIGNAL

    def update(self, signal_name: str, value: TradingAction):
        self.__last_signals[signal_name] = value

        if len(self.__config.input_signal_ids) != len(self.__last_signals):
            return

        self.__result = self._calculate(self.__last_signals)

    @abc.abstractmethod
    def _calculate(self, signals: typing.Dict[str, TradingAction]) -> TradingAction:  # pragma: no cover
        pass

    def read(self) -> TradingAction:
        return self.__result
