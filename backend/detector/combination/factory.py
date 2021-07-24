#!/usr/bin/python3

from config.detector import DetectorCombinationConfig

from detector.combination.and_combination import DetectorAndCombination
from detector.combination.or_combination import DetectorOrCombination
from detector.combination.not_combination import DetectorNotCombination


class InvalidDetectorCombinationType(Exception):
    pass


class DetectorCombinationFactory:
    @staticmethod
    def create(config: DetectorCombinationConfig):
        if config.combination_type == "and":
            return DetectorAndCombination(config)

        if config.combination_type == "or":
            return DetectorOrCombination(config)

        if config.combination_type == "not":
            return DetectorNotCombination(config)

        raise InvalidDetectorCombinationType()
