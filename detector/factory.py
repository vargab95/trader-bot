#!/usr/bin/python3

import logging

import config.market
import fetcher.single
import detector.interface
import detector.rising_edge
import detector.reverse_rising_edge
import detector.moving_threshold
import detector.falling_edge


class DetectorFactory:
    @classmethod
    def create(
        cls,
        configuration: config.market.MarketConfig,
        gatherer: fetcher.single.TradingViewFetcherSingle = None
    ) -> detector.interface.DetectorInterface:
        if configuration.falling_edge_detection:
            logging.info("Falling edge detector has been created.")
            return detector.falling_edge.FallingEdgeDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold)
        if gatherer:
            logging.info("Moving threshold detector has been created.")
            return detector.moving_threshold.MovingThresholdRisingEdgeDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold, gatherer)
        if configuration.bullish_threshold >= configuration.bearish_threshold:
            logging.info("Rising edge detector has been created.")
            return detector.rising_edge.RisingEdgeDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold)
        logging.info("Reverse rising_edge detector has been created.")
        return detector.reverse_rising_edge.ReverseRisingEdgeDetector(
            configuration.bearish_threshold, configuration.bullish_threshold)
