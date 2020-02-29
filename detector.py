#!/usr/bin/python3

import logging

from typing import Callable

import actions

class CrossOverDetector:
    def __init__(self, bullish: Callable, bearish: Callable):
        self.previous_summary: float = None
        self.bullish_callback: Callable = bullish
        self.bearish_callback: Callable = bearish

    def check_crossover(self, summary: float) -> actions.TradingAction:
        logging.info("Current state: %f", summary)
        if self.previous_summary:
            if summary == 0.0 and self.previous_summary == 0.0:
                pass
            if summary >= 0.0 and self.previous_summary <= 0.0:
                self.bullish_callback()
            elif summary <= 0.0 and self.previous_summary >= 0.0:
                self.bearish_callback()

        self.previous_summary = summary
