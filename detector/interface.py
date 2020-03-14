#!/usr/bin/python3

import abc
import actions


class DetectorInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, indicator: float) -> actions.TradingAction:
        pass

    @abc.abstractmethod
    def set_threshold(self, bearish_threshold: float,
                      bullish_threshold: float):
        pass
