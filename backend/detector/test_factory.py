#!/usr/bin/python3

import unittest

from detector.factory import DetectorFactory, InvalidDetectorConfiguration
from detector.falling_edge import FallingEdgeDetector
from detector.moving_threshold import MovingThresholdRisingEdgeDetector
from detector.rising_edge import RisingEdgeDetector
from detector.reverse_rising_edge import ReverseRisingEdgeDetector
from detector.stateless_rising_edge import StatelessRisingEdgeDetector
from detector.stateless_reverse_rising_edge import StatelessReverseRisingEdgeDetector
from detector.latched_reverse_rising_edge import LatchedReverseRisingEdgeDetector
from detector.latched_rising_edge import LatchedRisingEdgeDetector
from detector.simple_treshold import SimpleTresholdDetector
from detector.reverse_simple_treshold import ReverseSimpleTresholdDetector
from config.detector import DetectorConfig


class DetectorFactoryTest(unittest.TestCase):
    def test_create_falling_edge(self):
        config = DetectorConfig({})

        config.falling_edge = True
        config.bullish_threshold = 0.2
        config.bearish_threshold = 0.1

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

    def test_create_latched_reverse_rising_edge(self):
        config = DetectorConfig({})

        config.latched = True
        config.bearish_threshold = 0.4
        config.bullish_threshold = -0.4

        instance = DetectorFactory.create(config)
        self.assertIsInstance(instance, LatchedReverseRisingEdgeDetector)

    def test_create_latched_rising_edge(self):
        config = DetectorConfig({})

        config.latched = True
        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        instance = DetectorFactory.create(config)
        self.assertIsInstance(instance, LatchedRisingEdgeDetector)

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

    def test_create_stateless_falling_edge(self):
        config = DetectorConfig({})

        config.stateless = True
        config.falling_edge = True
        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        try:
            DetectorFactory.create(config)
            self.fail()
        except InvalidDetectorConfiguration:
            pass

    def test_create_stateless_follower(self):
        config = DetectorConfig({})

        config.stateless = True
        config.follower = True
        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        try:
            DetectorFactory.create(config)
            self.fail()
        except InvalidDetectorConfiguration:
            pass

    def test_simple_treshold(self):
        config = DetectorConfig({})

        config.simple = True
        config.bearish_threshold = -0.4
        config.bullish_threshold = 0.4

        self.assertIsInstance(DetectorFactory.create(config), SimpleTresholdDetector)

    def test_reverse_simple_treshold(self):
        config = DetectorConfig({})

        config.simple = True
        config.bearish_threshold = 0.4
        config.bullish_threshold = -0.4

        self.assertIsInstance(DetectorFactory.create(config), ReverseSimpleTresholdDetector)
