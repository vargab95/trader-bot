#!/usr/bin/python3

import logging

import fetcher.single
import detector.common
import detector.rising_edge


class MovingThresholdRisingEdgeDetector(detector.rising_edge.RisingEdgeDetector):
    def __init__(self, bearish_threshold: float, bullish_threshold: float,
                 gatherer: fetcher.single.TradingViewFetcherSingle):
        super().__init__(bearish_threshold, bullish_threshold)
        self.__original_bearish_threshold = bearish_threshold
        self.__original_bullish_threshold = bullish_threshold
        self.gatherer = gatherer
        self.first_signal_returned: bool = False

    @staticmethod
    def __saturate(value: float, threshold: float) -> float:
        if value > threshold:
            return threshold
        if value < (threshold * -1):
            return threshold * -1
        return value

    def check(self, indicator: float) -> detector.common.TradingAction:
        self.gatherer.fetch_technical_indicator()
        long_term_indicator = self.gatherer.get_technical_indicator()

        self.set_threshold(
            self.__saturate(self.__original_bearish_threshold -
                            long_term_indicator, 1.0),
            self.__saturate(self.__original_bullish_threshold - long_term_indicator, 1.0))

        logging.info(
            "New moving threshold: Long term = %f, Bearish = %f, Bullish = %f",
            long_term_indicator, self._bearish_threshold,
            self._bullish_threshold)

        result = super().check(indicator)
        logging.debug("New state of the moving threshold detector: %s",
                      str(result))

        if self.first_signal_returned:
            self._last_result = result
            return result

        self.first_signal_returned = True
        if indicator <= self._bearish_threshold:
            logging.debug("Initial state was overwritten by bearish")
            self._last_result = detector.common.TradingAction.BEARISH_SIGNAL
            return detector.common.TradingAction.BEARISH_SIGNAL

        if indicator >= self._bullish_threshold:
            logging.debug("Initial state was overwritten by bullish")
            self._last_result = detector.common.TradingAction.BULLISH_SIGNAL
            return detector.common.TradingAction.BULLISH_SIGNAL

        logging.debug("Initial state was overwritten by hold")
        self._last_result = detector.common.TradingAction.HOLD_SIGNAL
        return detector.common.TradingAction.HOLD_SIGNAL
