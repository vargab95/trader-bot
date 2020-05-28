#!/usr/bin/python3

import typing


class FilterConfig:
    def __init__(self, config: typing.Dict):
        self.type: str = config.get("type", "sma")
        self.length: int = config.get("length", 2)

    def __str__(self):
        return "\nFilter:" + \
               "\n    Type:   " + str(self.type) + \
               "\n    Length: " + str(self.length)
