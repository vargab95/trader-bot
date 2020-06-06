#!/usr/bin/python3

import typing

from config.detector import DetectorConfig


class TraderConfig:
    def __init__(self, config: typing.Dict):
        self.market = config.get("name", "GEMINI:BTCUSD")
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)
        self.max_steps = config.get("step_count", 5)
        self.detectors = [DetectorConfig(detector_config)
                          for detector_config in config.get("detectors", [])]

    def __str__(self):
        return "\nTrader:" + \
               "\n    Market:                 " + str(self.market) + \
               "\n    Indicator:              " + str(self.indicator) + \
               "\n    Candle size:            " + str(self.candle_size) + \
               "\n    Method:                 " + str(self.method) + \
               "\n    Leverage:               " + str(self.leverage) + \
               "\n    Step count:             " + str(self.max_steps) + \
               "\n    Check interval:         " + str(self.check_interval) + \
               "\n    Detectors:              " + str(self.detectors)
