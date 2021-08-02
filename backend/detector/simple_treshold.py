#!/usr/bin/python3

import detector.interface


class SimpleTresholdDetector(detector.interface.DetectorInterface):
    def check(self, indicator: float) -> detector.common.TradingAction:
        if indicator >= self._bullish_threshold:
            return detector.common.TradingAction.BULLISH_SIGNAL

        if indicator <= self._bearish_threshold:
            return detector.common.TradingAction.BEARISH_SIGNAL

        return detector.common.TradingAction.HOLD_SIGNAL
