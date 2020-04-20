#!/usr/bin/python3

import logging

import fetcher.single
import detector.interface
import detector.rising_edge
import detector.reverse_rising_edge
import detector.moving_threshold
import detector.falling_edge


class DetectorFactory:
    @classmethod
    def create(cls,
               bearish_threshold: float,
               bullish_threshold: float,
               falling_edge_detection: bool = False,
               gatherer: fetcher.single.TradingViewFetcherSingle = None):
        if falling_edge_detection:
            logging.info("Falling edge detector has been created.")
            return detector.falling_edge.FallingEdgeDetector(
                bearish_threshold, bullish_threshold)
        if gatherer:
            logging.info("Moving threshold detector has been created.")
            return detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                bearish_threshold, bullish_threshold, gatherer)
        if bullish_threshold >= bearish_threshold:
            logging.info("Rising edge detector has been created.")
            return detector.rising_edge.RisingEdgeDetector(
                bearish_threshold, bullish_threshold)
        logging.info("Reverse rising_edge detector has been created.")
        return detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            bearish_threshold, bullish_threshold)
