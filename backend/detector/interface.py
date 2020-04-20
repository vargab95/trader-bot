#!/usr/bin/python3

import abc

import detector.common


class DetectorInterface(metaclass=abc.ABCMeta):
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        self._bullish_threshold = bullish_threshold
        self._bearish_threshold = bearish_threshold

    @abc.abstractmethod
    def check(self, indicator: float) -> detector.common.TradingAction:
        pass  # pragma: no cover

    def set_threshold(self, bearish_threshold: float,
                      bullish_threshold: float):
        self._bullish_threshold = bullish_threshold
        self._bearish_threshold = bearish_threshold
