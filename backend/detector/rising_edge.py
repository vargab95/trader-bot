#!/usr/bin/python3

import logging

import detector.common


class RisingEdgeDetector:
    def __init__(self, bearish_threshold: float, bullish_threshold: float):
        self.current_state: detector.common.CurrentState = \
            detector.common.CurrentState.NONE
        self.bullish_threshold: float = bullish_threshold
        self.bearish_threshold: float = bearish_threshold

    def _bullish_compare(self, indicator):
        return indicator > self.bullish_threshold

    def _bearish_compare(self, indicator):
        return indicator < self.bearish_threshold

    def check(self, indicator: float) -> detector.common.TradingAction:
        result = detector.common.TradingAction.HOLD
        logging.info("Current state: %f", indicator)
        if self._bullish_compare(indicator) and \
                self.current_state != detector.common.CurrentState.BULL:
            logging.debug("Bullish trade was detected.")
            result = detector.common.TradingAction.SWITCH_TO_BULLISH
            self.current_state = detector.common.CurrentState.BULL
        elif self._bearish_compare(indicator) and \
                self.current_state != detector.common.CurrentState.BEAR:
            logging.debug("Bearish trade was detected.")
            result = detector.common.TradingAction.SWITCH_TO_BEARISH
            self.current_state = detector.common.CurrentState.BEAR

        return result
