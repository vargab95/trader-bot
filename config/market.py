#!/usr/bin/python3

import typing


class MarketConfig:
    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "GEMINI:BTCUSD")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.bullish_threshold = config.get("bullish_threshold", 0.0)
        self.bearish_threshold = config.get("bullish_threshold", 0.0)

    def __str__(self):
        return "\nMarket:" + \
               "\n    Name:              " + self.name + \
               "\n    Candle size:       " + self.candle_size + \
               "\n    Check interval:    " + str(self.check_interval) + \
               "\n    Bullish threshold: " + str(self.bullish_threshold) + \
               "\n    Bearish threshold: " + str(self.bearish_threshold)
