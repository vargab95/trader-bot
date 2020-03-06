#!/usr/bin/python3

import abc
import typing

class DetectorInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check(self, summary: float) -> actions.TradingAction:
        pass

    @abc.abstractmethod
    def set_threshold(bearish_threshold: float, bullish_threshold: float):
        pass
