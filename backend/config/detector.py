#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class DetectorConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.input_signal_id = config.get("input_signal_id", None)
        self.output_signal_id = config.get("output_signal_id", None)
        self.follower = config.get("follower", False)
        self.follower_candle_size = config.get("follower_candle_size", None)
        self.falling_edge = config.get("falling_edge", False)
        self.stateless = config.get("stateless", False)
        self.latched = config.get("latched", False)
        self.simple = config.get("simple", False)
        self.bullish_threshold = config.get("bullish_threshold", None)
        self.bearish_threshold = config.get("bearish_threshold", None)

    def validate(self):
        if self.input_signal_id is None:
            raise InvalidConfigurationException("Input signal id is mandatory in detector config")

        if self.output_signal_id is None:
            raise InvalidConfigurationException("Output signal id is mandatory in detector config")

        if self.bearish_threshold is None:
            raise InvalidConfigurationException("Bearish treshold id is mandatory in detector config")

        if self.bullish_threshold is None:
            raise InvalidConfigurationException("Bullish treshold id is mandatory in detector config")

        if self.follower and self.follower_candle_size is None:
            raise InvalidConfigurationException("Follower candle size must be specified is follower mode is enabled")


class DetectorCombinationConfig(ConfigComponentBase):
    available_combination_types = ["and", "or", "not"]

    def __init__(self, config: typing.Dict):
        self.input_signal_ids = config.get("input_signal_ids", None)
        self.output_signal_id = config.get("output_signal_id", None)
        self.combination_type = config.get("combination_type", None)

    def __str__(self):
        return "\n        Detector:" + \
               "\n            Input signal ids:       " + str(self.input_signal_ids) + \
               "\n            Output signal id:       " + str(self.output_signal_id) + \
               "\n            Combination type:       " + str(self.combination_type)

    def validate(self):
        if self.input_signal_ids is None:
            raise InvalidConfigurationException("Input signal ids is mandatory in detector combination logic config")

        if self.output_signal_id is None:
            raise InvalidConfigurationException("Output signal id is mandatory in detector combination logic config")

        if self.combination_type is None:
            raise InvalidConfigurationException("Combination type is mandatory in detector combination logic config")

        if self.combination_type not in self.available_combination_types:
            raise InvalidConfigurationException(f"{self.combination_type} is not allowed.")
