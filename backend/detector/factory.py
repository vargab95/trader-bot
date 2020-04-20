#!/usr/bin/python3

import logging

import fetcher.single
import detector.interface
import detector.rising_edge
import detector.reverse_rising_edge
import detector.moving_threshold
import detector.falling_edge
from detector.stateless_rising_edge import StatelessRisingEdgeDetector
from detector.stateless_reverse_rising_edge \
        import StatelessReverseRisingEdgeDetector


class InvalidDetectorConfiguration(Exception):
    pass


class DetectorFactory:
    @classmethod
    def create(cls,
               bearish_threshold: float,
               bullish_threshold: float,
               falling_edge_detection: bool = False,
               use_stateless_detector: bool = False,
               gatherer: fetcher.single.TradingViewFetcherSingle = None):
        if falling_edge_detection:
            if use_stateless_detector:
                raise InvalidDetectorConfiguration

            logging.info("Falling edge detector has been created.")
            return detector.falling_edge.FallingEdgeDetector(
                bearish_threshold, bullish_threshold)

        if gatherer:
            if use_stateless_detector:
                raise InvalidDetectorConfiguration

            logging.info("Moving threshold detector has been created.")
            return detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                bearish_threshold, bullish_threshold, gatherer)

        if bullish_threshold >= bearish_threshold:
            if use_stateless_detector:
                logging.info(
                    "Stateless rising edge detector has been created.")
                return StatelessRisingEdgeDetector(bearish_threshold,
                                                   bullish_threshold)

            logging.info("Rising edge detector has been created.")
            return detector.rising_edge.RisingEdgeDetector(
                bearish_threshold, bullish_threshold)

        if use_stateless_detector:
            logging.info("Stateless reverse rising_edge detector"
                         " has been created.")
            return StatelessReverseRisingEdgeDetector(bearish_threshold,
                                                      bullish_threshold)

        logging.info("Reverse rising_edge detector has been created.")
        return detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            bearish_threshold, bullish_threshold)
