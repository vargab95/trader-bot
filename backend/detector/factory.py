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
from config.detector import DetectorConfig


class InvalidDetectorConfiguration(Exception):
    pass


class DetectorFactory:
    @staticmethod
    def create(configuration: DetectorConfig, gatherer: fetcher.single.TradingViewFetcherSingle = None):
        if configuration.falling_edge:
            if configuration.stateless:
                raise InvalidDetectorConfiguration

            logging.info("Falling edge detector has been created.")
            return detector.falling_edge.FallingEdgeDetector(configuration.bearish_threshold,
                                                             configuration.bullish_threshold)

        if configuration.follower:
            if configuration.stateless:
                raise InvalidDetectorConfiguration

            logging.info("Moving threshold detector has been created.")
            return detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                configuration.bearish_threshold, configuration.bullish_threshold, gatherer)

        if configuration.bullish_threshold >= configuration.bearish_threshold:
            if configuration.stateless:
                logging.info(
                    "Stateless rising edge detector has been created.")
                return StatelessRisingEdgeDetector(configuration.bearish_threshold,
                                                   configuration.bullish_threshold)

            logging.info("Rising edge detector has been created.")
            return detector.rising_edge.RisingEdgeDetector(
                configuration.bearish_threshold, configuration.bullish_threshold)

        if configuration.stateless:
            logging.info("Stateless reverse rising_edge detector"
                         " has been created.")
            return StatelessReverseRisingEdgeDetector(configuration.bearish_threshold,
                                                      configuration.bullish_threshold)

        logging.info("Reverse rising_edge detector has been created.")
        return detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            configuration.bearish_threshold, configuration.bullish_threshold)
