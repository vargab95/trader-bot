#!/usr/bin/python3

import typing

from config.detector import DetectorConfig
from config.filter import FilterConfig

from trader.common import TraderState


class TraderConfig:
    def __init__(self, config: typing.Dict):
        self.input_signal_id = config.get("input_signal_id", None)
        self.market = config.get("market", "GEMINI:BTCUSD")
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)
        # TODO Process it using string not int
        self.start_state = TraderState(config.get("start_state", TraderState.BASE))
        self.max_steps = config.get("max_steps", 5)
        self.initial_values = config.get("initial_values", [])
        self.detectors = [DetectorConfig(detector_config)
                          for detector_config in config.get("detectors", [])]
        self.filters = [FilterConfig(filter_element)
                        for filter_element in config.get("filters", [])]
        self.initial_length = config.get("initial_length", 1)
        self.initial_keyword = config.get("initial_keyword", "close")
        self.initial_step = config.get("initial_step", 1)

    def __str__(self):
        return "\nTrader:" + \
               "\n    Input signal id:             " + str(self.input_signal_id) + \
               "\n    Market:                      " + str(self.market) + \
               "\n    Indicator:                   " + str(self.indicator) + \
               "\n    Candle size:                 " + str(self.candle_size) + \
               "\n    Method:                      " + str(self.method) + \
               "\n    Leverage:                    " + str(self.leverage) + \
               "\n    Start state:                 " + str(self.start_state) + \
               "\n    Step count:                  " + str(self.max_steps) + \
               "\n    Check interval:              " + str(self.check_interval) + \
               "\n    Detectors:                   " + \
               ''.join([str(detector) for detector in self.detectors]) + \
               "\n    Filters:                     " + \
               ''.join([str(f) for f in self.filters]) + \
               "\n    Initialization list length:  " + str(self.initial_length) + \
               "\n    Initialization list keyword: " + \
               str(self.initial_keyword)
