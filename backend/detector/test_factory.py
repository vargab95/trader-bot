#!/usr/bin/python3

import unittest

from detector.factory import DetectorFactory
from detector.falling_edge import FallingEdgeDetector
from detector.moving_threshold import MovingThresholdRisingEdgeDetector
from detector.rising_edge import RisingEdgeDetector
from detector.reverse_rising_edge import ReverseRisingEdgeDetector
from detector.stateless_rising_edge import StatelessRisingEdgeDetector
from detector.stateless_reverse_rising_edge import StatelessReverseRisingEdgeDetector
from config.detector import DetectorConfig


class FilterFactoryTest(unittest.TestCase):
    def test_create_falling_edge(self):
        config = DetectorConfig({})

        config.falling_edge = True

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(instance, FallingEdgeDetector))

    def test_create_moving_threshold(self):
        config = DetectorConfig({})

        config.follower = True

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(
            instance, MovingThresholdRisingEdgeDetector))

    def test_create_reverse_rising_edge(self):
        config = DetectorConfig({})

        config.bearish_threshold = 0.4
        config.bullish_threshold = -0.4

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(
            instance, ReverseRisingEdgeDetector))

    def test_create_rising_edge(self):
        config = DetectorConfig({})

        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(
            instance, RisingEdgeDetector))

    def test_create_stateless_reverse_rising_edge(self):
        config = DetectorConfig({})

        config.stateless = True
        config.bearish_threshold = 0.4
        config.bullish_threshold = -0.4

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(
            instance, StatelessReverseRisingEdgeDetector))

    def test_create_stateless_rising_edge(self):
        config = DetectorConfig({})

        config.stateless = True
        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        instance = DetectorFactory.create(config)
        self.assertTrue(isinstance(
            instance, StatelessRisingEdgeDetector))