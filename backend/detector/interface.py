#!/usr/bin/python3

import abc

import detector.common


class DetectorInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, indicator: float) -> detector.common.TradingAction:
        pass

    @abc.abstractmethod
    def set_threshold(self, bearish_threshold: float,
                      bullish_threshold: float):
        pass
