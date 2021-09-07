#!/usr/bin/python3

import detector.interface


class ReverseSimpleTresholdDetector(detector.interface.DetectorInterface):
    def check(self, indicator: float) -> detector.common.TradingAction:
        if indicator <= self._bullish_threshold:
            self._last_result = detector.common.TradingAction.BULLISH_SIGNAL
            return detector.common.TradingAction.BULLISH_SIGNAL

        if indicator >= self._bearish_threshold:
            self._last_result = detector.common.TradingAction.BEARISH_SIGNAL
            return detector.common.TradingAction.BEARISH_SIGNAL

        self._last_result = detector.common.TradingAction.HOLD_SIGNAL
        return detector.common.TradingAction.HOLD_SIGNAL
