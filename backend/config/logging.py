#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class LoggingConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        # Log level. For details, check https://docs.python.org/3/howto/logging.html#logging-levels
        self.level: int = config.get("level", 31)

        # Log file path. If omitted, then logs are printed to the console
        self.path: str = config.get("path", None)

    def validate(self):
        pass
