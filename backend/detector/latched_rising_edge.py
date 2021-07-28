#!/usr/bin/python3

import detector.common
import detector.interface


class LatchedRisingEdgeDetector(detector.interface.DetectorInterface):
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        super().__init__(bearish_threshold, bullish_threshold)
        self._last_value = (bearish_threshold + bullish_threshold) / 2.0
        self._result = detector.common.TradingAction.HOLD_SIGNAL

    def _bullish_compare(self, indicator):
        return indicator > self._bullish_threshold and \
            self._last_value <= self._bullish_threshold and \
            indicator != self._last_value

    def _bearish_compare(self, indicator):
        return indicator < self._bearish_threshold and \
            self._last_value >= self._bearish_threshold and \
            indicator != self._last_value

    def check(self, indicator: float) -> detector.common.TradingAction:
        if self._bullish_compare(indicator):
            self._result = detector.common.TradingAction.BULLISH_SIGNAL
        elif self._bearish_compare(indicator):
            self._result = detector.common.TradingAction.BEARISH_SIGNAL

        self._last_value = indicator

        return self._result
