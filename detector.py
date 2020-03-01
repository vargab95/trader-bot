#!/usr/bin/python3

import logging

from typing import Callable

import actions

class CrossOverDetector:
    def __init__(self):
        self.previous_summary: float = 0.0
        self.bullish_threshold: float = 0.0
        self.bearish_threshold: float = 0.0

    def check_crossover(self, summary: float) -> actions.TradingAction:
        result = actions.TradingAction.HOLD
        logging.info("Current state: %f", summary)
        if summary > self.bullish_threshold and self.previous_summary <= self.bullish_threshold:
            logging.debug("Bullish trade was detected.")
            result = actions.TradingAction.SWITCH_TO_BULLISH
        elif summary < self.bearish_threshold and self.previous_summary >= self.bearish_threshold:
            logging.debug("Bearish trade was detected.")
            result = actions.TradingAction.SWITCH_TO_BEARISH

        self.previous_summary = summary
        return result
