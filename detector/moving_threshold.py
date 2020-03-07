#!/usr/bin/python3

import spider
import actions
import detector.common
import detector.crossover


class MovingThresholdCrossOverDetector(detector.crossover.CrossOverDetector):
    def __init__(self, bearish_threshold: float, bullish_threshold: float,
                 gatherer: spider.TradingViewSpider):
        super().__init__(bearish_threshold, bullish_threshold)
        self.original_bearish_threshold = bearish_threshold
        self.original_bullish_threshold = bullish_threshold
        self.gatherer = gatherer

    @staticmethod
    def __saturate(value: float, threshold: float) -> float:
        if value > threshold:
            return threshold
        if value < (threshold * -1):
            return threshold * -1
        return value

    def check(self, summary: float) -> actions.TradingAction:
        long_term_summary = self.gatherer.get_technical_summary()

        self.bearish_threshold = self.__saturate(
            self.original_bearish_threshold - long_term_summary, 1.0)
        self.bullish_threshold = self.__saturate(
            self.original_bullish_threshold - long_term_summary, 1.0)

        return super().check(summary)
