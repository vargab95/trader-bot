#!/usr/bin/python3

import detector.common
import detector.interface


class RisingEdgeDetector(detector.interface.DetectorInterface):
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        super().__init__(bearish_threshold, bullish_threshold)
        self.current_state: detector.common.CurrentState = detector.common.CurrentState.NONE

    def _bullish_compare(self, indicator):
        return indicator > self._bullish_threshold

    def _bearish_compare(self, indicator):
        return indicator < self._bearish_threshold

    def check(self, indicator: float) -> detector.common.TradingAction:
        result = detector.common.TradingAction.HOLD_SIGNAL
        if self._bullish_compare(indicator) and self.current_state != detector.common.CurrentState.BULL:
            result = detector.common.TradingAction.BULLISH_SIGNAL
            self.current_state = detector.common.CurrentState.BULL
        elif self._bearish_compare(indicator) and self.current_state != detector.common.CurrentState.BEAR:
            result = detector.common.TradingAction.BEARISH_SIGNAL
            self.current_state = detector.common.CurrentState.BEAR

        return result
