#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class FilterConfig(ConfigComponentBase):
    available_types = ["sma", "hma", "wma", "nth", "derivative", "derivative_ratio", "rsi", "macd"]

    def __init__(self, config: typing.Dict):
        self.input_signal_id: str = config.get("input_signal_id", None)
        self.output_signal_id: str = config.get("output_signal_id", None)
        self.type: str = config.get("type", "sma")
        self.length: int = config.get("length", None)
        self.second_length: int = config.get("second_length", None)

    def validate(self):
        if self.input_signal_id is None:
            raise InvalidConfigurationException("Input signal id is a mandatory parameter for filters")

        if self.output_signal_id is None:
            raise InvalidConfigurationException("Output signal id is a mandatory parameter for filters")

        if self.type not in self.available_types:
            raise InvalidConfigurationException(f"{self.type} is not a valid filter type")

        if self.length is None or self.length < 2:
            raise InvalidConfigurationException(f"{self.length} is not a valid filter length")

        if self.type == "macd" and self.second_length is None:
            raise InvalidConfigurationException("Second length have to be specified for macd")
