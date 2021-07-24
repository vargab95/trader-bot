#!/usr/bin/python3

import typing


class FilterConfig:
    def __init__(self, config: typing.Dict):
        self.input_signal_id: str = config.get("input_signal_id", None)
        self.output_signal_id: str = config.get("output_signal_id", None)
        self.type: str = config.get("type", "sma")
        self.length: int = config.get("length", 2)

    def __str__(self):
        return "\n        Filter:" + \
               "\n            Type:   " + str(self.type) + \
               "\n            Length: " + str(self.length)
