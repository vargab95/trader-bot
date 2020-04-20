#!/usr/bin/python3

import detector.rising_edge


class ReverseRisingEdgeDetector(detector.rising_edge.RisingEdgeDetector):
    def _bullish_compare(self, indicator):
        return indicator < self._bullish_threshold

    def _bearish_compare(self, indicator):
        return indicator > self._bearish_threshold
