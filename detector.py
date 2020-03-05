#!/usr/bin/python3

import logging
import enum

from typing import Callable

import actions

class CurrentState(enum.Enum):
    NONE = 0
    BEAR = 1
    BULL = 2

class CrossOverDetector:
    def __init__(self, bearish_threshold: float = 0.0, bullish_threshold: float = 0.0):
        self.current_state: CurrentState = CurrentState.NONE
        self.bullish_threshold: float = bullish_threshold
        self.bearish_threshold: float = bearish_threshold
        self.previous_summary: float = (bullish_threshold + bearish_threshold) / 2

    def check_crossover(self, summary: float) -> actions.TradingAction:
        result = actions.TradingAction.HOLD
        logging.info("Current state: %f", summary)
        if summary > self.bullish_threshold and \
                self.previous_summary <= self.bullish_threshold and \
                self.current_state != CurrentState.BULL:
            logging.debug("Bullish trade was detected.")
            result = actions.TradingAction.SWITCH_TO_BULLISH
            self.current_state = CurrentState.BULL
        elif summary < self.bearish_threshold and \
                self.previous_summary >= self.bearish_threshold and \
                self.current_state != CurrentState.BEAR:
            logging.debug("Bearish trade was detected.")
            result = actions.TradingAction.SWITCH_TO_BEARISH
            self.current_state = CurrentState.BEAR

        self.previous_summary = summary
        return result
