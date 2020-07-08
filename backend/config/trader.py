#!/usr/bin/python3

import typing

from config.detector import DetectorConfig
from config.filter import FilterConfig


class TraderConfig:
    def __init__(self, config: typing.Dict):
        self.market = config.get("market", "GEMINI:BTCUSD")
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)
        self.max_steps = config.get("max_steps", 5)
        self.initial_values = config.get("initial_values", [])
        self.detectors = [DetectorConfig(detector_config)
                          for detector_config in config.get("detectors", [])]
        self.filters = [FilterConfig(filter_element)
                        for filter_element in config.get("filter", [])]
        self.initial_length = config.get("initial_length", 1)
        self.initial_keyword = config.get("initial_keyword", "close")

    def __str__(self):
        return "\nTrader:" + \
               "\n    Market:                      " + str(self.market) + \
               "\n    Indicator:                   " + str(self.indicator) + \
               "\n    Candle size:                 " + str(self.candle_size) + \
               "\n    Method:                      " + str(self.method) + \
               "\n    Leverage:                    " + str(self.leverage) + \
               "\n    Step count:                  " + str(self.max_steps) + \
               "\n    Check interval:              " + str(self.check_interval) + \
               "\n    Detectors:                   " + \
            ', '.join([str(detector) for detector in self.detectors]) + \
               "\n    Filters:                     " + \
            ', '.join([str(filter) for filter in self.filters]) + \
               "\n    Initialization list length:  " + str(self.initial_length) + \
               "\n    Initialization list keyword: " + \
            str(self.initial_keyword)
