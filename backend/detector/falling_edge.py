#!/usr/bin/python3

import detector.common
import detector.interface


class FallingEdgeDetector(detector.interface.DetectorInterface):
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        super().__init__(bearish_threshold, bullish_threshold)
        self.current_state: detector.common.CurrentState = \
            detector.common.CurrentState.NONE
        self.previous_indicator: float = (bullish_threshold +
                                          bearish_threshold) / 2

    def check(self, indicator: float) -> detector.common.TradingAction:
        result = detector.common.TradingAction.HOLD
        if indicator >= self._bullish_threshold and \
                self.previous_indicator <= self._bullish_threshold and \
                self.current_state != detector.common.CurrentState.BULL:
            result = detector.common.TradingAction.BUY_BULLISH
            self.current_state = detector.common.CurrentState.BULL
        elif indicator <= self._bearish_threshold and \
                self.previous_indicator >= self._bearish_threshold and \
                self.current_state != detector.common.CurrentState.BEAR:
            result = detector.common.TradingAction.BUY_BEARISH
            self.current_state = detector.common.CurrentState.BEAR

        self.previous_indicator = indicator
        return result
