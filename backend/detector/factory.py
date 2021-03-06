#!/usr/bin/python3

import logging

import fetcher.single
import detector.interface
import detector.rising_edge
import detector.reverse_rising_edge
import detector.moving_threshold
import detector.falling_edge
from detector.latched_rising_edge import LatchedRisingEdgeDetector
from detector.latched_reverse_rising_edge import LatchedReverseRisingEdgeDetector
from detector.stateless_rising_edge import StatelessRisingEdgeDetector
from detector.stateless_reverse_rising_edge import StatelessReverseRisingEdgeDetector
from detector.simple_treshold import SimpleTresholdDetector
from detector.reverse_simple_treshold import ReverseSimpleTresholdDetector
from detector.reset_on_falling_edge import ResetOnFallingEdgeDetector
from config.detector import DetectorConfig


class InvalidDetectorConfiguration(Exception):
    pass


class DetectorFactory:
    @staticmethod
    def create(configuration: DetectorConfig, gatherer: fetcher.single.TradingViewFetcherSingle = None):
        if configuration.reset_on_falling_edge:
            logging.info("Reset on falling edge detector created")
            return ResetOnFallingEdgeDetector(configuration.bearish_threshold, configuration.bullish_threshold)

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
            if configuration.simple:
                return SimpleTresholdDetector(configuration.bearish_threshold, configuration.bullish_threshold)

            if configuration.stateless:
                logging.info("Stateless rising edge detector has been created.")
                return StatelessRisingEdgeDetector(configuration.bearish_threshold,
                                                   configuration.bullish_threshold)

            if configuration.latched:
                logging.info("Latched rising edge detector has been created.")
                return LatchedRisingEdgeDetector(configuration.bearish_threshold, configuration.bullish_threshold)

            logging.info("Rising edge detector has been created.")
            return detector.rising_edge.RisingEdgeDetector(configuration.bearish_threshold,
                                                           configuration.bullish_threshold)

        if configuration.simple:
            return ReverseSimpleTresholdDetector(configuration.bearish_threshold, configuration.bullish_threshold)

        if configuration.stateless:
            logging.info("Stateless reverse rising edge detector has been created.")
            return StatelessReverseRisingEdgeDetector(configuration.bearish_threshold,
                                                      configuration.bullish_threshold)

        if configuration.latched:
            logging.info("Latched reverse rising edge detector has been created.")
            return LatchedReverseRisingEdgeDetector(configuration.bearish_threshold,
                                                    configuration.bullish_threshold)

        logging.info("Reverse rising edge detector has been created.")
        return detector.reverse_rising_edge.ReverseRisingEdgeDetector(configuration.bearish_threshold,
                                                                      configuration.bullish_threshold)
