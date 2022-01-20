#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class DatabaseConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        # URL of the mongodb instance
        self.url = config.get("url", None)

        # User of the mongodb instance
        self.user = config.get("user", None)

        # Password of mongodb user
        self.password = config.get("password", None)

        # Limit for number of requested data points
        self.limit = config.get("limit", -1)

    def validate(self):
        if self.url is None:
            return

        if self.user is None or self.password is None:
            raise InvalidConfigurationException("If database url is filled credentials should also be specified")
