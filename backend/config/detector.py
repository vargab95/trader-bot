#!/usr/bin/python3

import typing


class DetectorConfig:
    def __init__(self, config: typing.Dict):
        self.follower = config.get("follower", False)
        self.follower_candle_size = config.get("follower_candle_size", "1h")
        self.falling_edge = config.get("falling_edge",
                                       False)
        self.stateless = config.get("stateless", False)
        self.bullish_threshold = config.get("bullish_threshold", 0.0)
        self.bearish_threshold = config.get("bearish_threshold", 0.0)

    def __str__(self):
        return "\n    Detector:" + \
               "\n        Follower enabled:       " + str(self.follower) + \
               "\n        Follower candle size:   " + str(self.follower_candle_size) + \
               "\n        Falling edge detection: " + str(self.falling_edge) + \
               "\n        Stateless:              " + str(self.stateless) + \
               "\n        Bullish threshold:      " + str(self.bullish_threshold) + \
               "\n        Bearish threshold:      " + \
            str(self.bearish_threshold)
