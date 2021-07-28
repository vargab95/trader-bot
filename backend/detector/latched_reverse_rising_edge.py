#!/usr/bin/python3

import detector.latched_rising_edge


class LatchedReverseRisingEdgeDetector(detector.latched_rising_edge.LatchedRisingEdgeDetector):
    def _bullish_compare(self, indicator):
        return indicator < self._bullish_threshold and \
               self._last_value >= self._bullish_threshold and \
               indicator != self._last_value

    def _bearish_compare(self, indicator):
        return indicator > self._bearish_threshold and \
               self._last_value <= self._bearish_threshold and \
               indicator != self._last_value
