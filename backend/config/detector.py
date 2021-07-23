#!/usr/bin/python3

import typing


class DetectorConfig:
    def __init__(self, config: typing.Dict):
        self.input_signal_id = config.get("input_signal_id", None)
        self.output_signal_id = config.get("output_signal_id", None)
        self.follower = config.get("follower", False)
        self.follower_candle_size = config.get("follower_candle_size", "1h")
        self.falling_edge = config.get("falling_edge",
                                       False)
        self.stateless = config.get("stateless", False)
        self.bullish_threshold = config.get("bullish_threshold", 0.0)
        self.bearish_threshold = config.get("bearish_threshold", 0.0)

    def __str__(self):
        return "\n        Detector:" + \
               "\n            Input signal id:        " + str(self.input_signal_id) + \
               "\n            Output signal id:       " + str(self.output_signal_id) + \
               "\n            Follower enabled:       " + str(self.follower) + \
               "\n            Follower candle size:   " + str(self.follower_candle_size) + \
               "\n            Falling edge detection: " + str(self.falling_edge) + \
               "\n            Stateless:              " + str(self.stateless) + \
               "\n            Bullish threshold:      " + str(self.bullish_threshold) + \
               "\n            Bearish threshold:      " + \
            str(self.bearish_threshold)


class DetectorCombinationConfig:
    def __init__(self, config: typing.Dict):
        self.input_signal_ids = config.get("input_signal_ids", None)
        self.output_signal_id = config.get("output_signal_id", None)
        self.combination_type = config.get("combination_type", None)

    def __str__(self):
        return "\n        Detector:" + \
               "\n            Input signal ids:       " + str(self.input_signal_ids) + \
               "\n            Output signal id:       " + str(self.output_signal_id) + \
               "\n            Combination type:       " + str(self.combination_type)
