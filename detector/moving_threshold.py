#!/usr/bin/python3

import logging

import fetcher
import actions
import detector.common
import detector.crossover


class MovingThresholdCrossOverDetector(detector.crossover.CrossOverDetector):
    def __init__(self, bearish_threshold: float, bullish_threshold: float,
                 gatherer: fetcher.TradingViewFetcher):
        super().__init__(bearish_threshold, bullish_threshold)
        self.original_bearish_threshold = bearish_threshold
        self.original_bullish_threshold = bullish_threshold
        self.gatherer = gatherer
        self.first_signal_returned: bool = False

    @staticmethod
    def __saturate(value: float, threshold: float) -> float:
        if value > threshold:
            return threshold
        if value < (threshold * -1):
            return threshold * -1
        return value

    def check(self, summary: float) -> actions.TradingAction:
        self.gatherer.fetch_technical_summary()
        long_term_summary = self.gatherer.get_technical_summary()

        self.bearish_threshold = self.__saturate(
            self.original_bearish_threshold - long_term_summary, 1.0)
        self.bullish_threshold = self.__saturate(
            self.original_bullish_threshold - long_term_summary, 1.0)

        logging.info(
            "New moving threshold: Long term = %f, Bearish = %f, Bullish = %f",
            long_term_summary, self.bearish_threshold, self.bullish_threshold)

        result = super().check(summary)
        logging.debug("New state of the moving threshold detector: %s",
                      str(result))

        if self.first_signal_returned:
            return result

        self.first_signal_returned = True
        if summary <= self.bearish_threshold:
            logging.debug("Initial state was overwritten by bearish")
            return actions.TradingAction.SWITCH_TO_BEARISH

        if summary >= self.bullish_threshold:
            logging.debug("Initial state was overwritten by bullish")
            return actions.TradingAction.SWITCH_TO_BULLISH

        logging.debug("Initial state was overwritten by hold")
        return actions.TradingAction.HOLD
