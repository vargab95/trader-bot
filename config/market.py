#!/usr/bin/python3

import typing


class MarketConfig:
    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "GEMINI:BTCUSD")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.summary_sma = config.get("summary_sma", 1)
        self.follower_enabled = config.get("follower_enabled", False)
        self.follower_candle_size = config.get("follower_candle_size", "1h")
        self.falling_edge_detection = config.get("falling_edge_detection", False)
        self.bullish_threshold = config.get("bullish_threshold", 0.0)
        self.bearish_threshold = config.get("bearish_threshold", 0.0)

    def __str__(self):
        return "\nMarket:" + \
               "\n    Name:                   " + self.name + \
               "\n    Candle size:            " + self.candle_size + \
               "\n    Summary SMA:            " + str(self.summary_sma) + \
               "\n    Follower enabled:       " + str(self.follower_enabled) + \
               "\n    Follower candle size:   " + self.follower_candle_size + \
               "\n    Check interval:         " + str(self.check_interval) + \
               "\n    Falling edge detection: " + str(self.falling_edge_detection) + \
               "\n    Bullish threshold:      " + str(self.bullish_threshold) + \
               "\n    Bearish threshold:      " + str(self.bearish_threshold)
