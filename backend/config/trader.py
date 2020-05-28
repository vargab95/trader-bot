#!/usr/bin/python3

import typing


class TraderConfig:
    def __init__(self, config: typing.Dict):
        # TODO create sub config classes
        self.market = config.get("name", "GEMINI:BTCUSD")
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.indicator_sma = config.get("indicator_sma", 1)
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)
        self.max_steps = config.get("step_count", 5)
        self.follower_enabled = config.get("follower_enabled", False)
        self.follower_candle_size = config.get("follower_candle_size", "1h")
        self.falling_edge_detection = config.get("falling_edge_detection",
                                                 False)
        self.thresholds = config.get("thresholds", [{
            "bear": 0.0,
            "bull": 0.0
        }])

    def __str__(self):
        return "\nTrader:" + \
               "\n    Market:                 " + str(self.market) + \
               "\n    Indicator:              " + str(self.indicator) + \
               "\n    Candle size:            " + str(self.candle_size) + \
               "\n    Summary SMA:            " + str(self.indicator_sma) + \
               "\n    Follower enabled:       " + str(self.follower_enabled) + \
               "\n    Follower candle size:   " + str(self.follower_candle_size) + \
               "\n    Method:                 " + str(self.method) + \
               "\n    Leverage:               " + str(self.leverage) + \
               "\n    Step count:             " + str(self.max_steps) + \
               "\n    Check interval:         " + str(self.check_interval) + \
               "\n    Falling edge detection: " + str(self.falling_edge_detection) + \
               "\n    Threshold:              " + str(self.thresholds)
