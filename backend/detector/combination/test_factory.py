#!/usr/bin/python3

import unittest

from detector.combination.factory import DetectorCombinationFactory, InvalidDetectorCombinationType
from detector.combination.and_combination import DetectorAndCombination
from detector.combination.or_combination import DetectorOrCombination
from detector.combination.not_combination import DetectorNotCombination
from config.detector import DetectorCombinationConfig


class TestDetectorCombinationFactory(unittest.TestCase):
    def test_create_and_combination(self):
        instance = DetectorCombinationFactory.create(DetectorCombinationConfig({"combination_type": "and"}))
        self.assertIsInstance(instance, DetectorAndCombination)

    def test_create_or_combination(self):
        instance = DetectorCombinationFactory.create(DetectorCombinationConfig({"combination_type": "or"}))
        self.assertIsInstance(instance, DetectorOrCombination)

    def test_create_not_combination(self):
        instance = DetectorCombinationFactory.create(DetectorCombinationConfig({"combination_type": "not"}))
        self.assertIsInstance(instance, DetectorNotCombination)

    def test_create_invalid(self):
        with self.assertRaises(InvalidDetectorCombinationType):
            DetectorCombinationFactory.create(DetectorCombinationConfig({"combination_type": "invalid"}))
