#!/usr/bin/python3

import logging

import config.market
import fetcher
import detector.interface
import detector.crossover
import detector.reverse_crossover
import detector.moving_threshold
import detector.falling_edge


class DetectorFactory:
    @classmethod
    def create(
        cls,
        configuration: config.market.MarketConfig,
        gatherer: fetcher.TradingViewFetcher = None
    ) -> detector.interface.DetectorInterface:
        if configuration.falling_edge_detection:
            logging.info("Falling edge detector has been created.")
            return detector.falling_edge.FallingEdgeDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold)
        if gatherer:
            logging.info("Moving threshold detector has been created.")
            return detector.moving_threshold.MovingThresholdCrossOverDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold, gatherer)
        if configuration.bullish_threshold >= configuration.bearish_threshold:
            logging.info("Crossover detector has been created.")
            return detector.crossover.CrossOverDetector(
                configuration.bearish_threshold,
                configuration.bullish_threshold)
        logging.info("Reverse crossover detector has been created.")
        return detector.reverse_crossover.ReverseCrossOverDetector(
            configuration.bearish_threshold, configuration.bullish_threshold)
