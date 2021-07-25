#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class LoggingConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.level: int = config.get("level", 31)
        self.path: str = config.get("path", "")

    def __str__(self):
        return "\nLogging:" + \
               "\n    Level: " + str(self.level) + \
               "\n    Path:  " + str(self.path)

    def validate(self):
        pass
