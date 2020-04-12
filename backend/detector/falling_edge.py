#!/usr/bin/python3

import logging

import detector.common


class FallingEdgeDetector:
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        self.current_state: detector.common.CurrentState = \
            detector.common.CurrentState.NONE
        self.bullish_threshold: float = bullish_threshold
        self.bearish_threshold: float = bearish_threshold
        self.previous_indicator: float = (bullish_threshold +
                                          bearish_threshold) / 2

    def check(self, indicator: float) -> detector.common.TradingAction:
        result = detector.common.TradingAction.HOLD
        logging.info("Current state: %f", indicator)
        if indicator >= self.bullish_threshold and \
                self.previous_indicator <= self.bullish_threshold and \
                self.current_state != detector.common.CurrentState.BULL:
            logging.debug("Bullish trade was detected.")
            result = detector.common.TradingAction.SWITCH_TO_BULLISH
            self.current_state = detector.common.CurrentState.BULL
        elif indicator <= self.bearish_threshold and \
                self.previous_indicator >= self.bearish_threshold and \
                self.current_state != detector.common.CurrentState.BEAR:
            logging.debug("Bearish trade was detected.")
            result = detector.common.TradingAction.SWITCH_TO_BEARISH
            self.current_state = detector.common.CurrentState.BEAR

        self.previous_indicator = indicator
        return result
