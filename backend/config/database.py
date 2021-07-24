#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class DatabaseConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.url = config.get("url", None)
        self.user = config.get("user", None)
        self.password = config.get("password", None)
        self.limit = config.get("limit", -1)

    def __str__(self):
        return "\nDatabase:" + \
               "\n    URL:         " + self.url + \
               "\n    Username:    " + self.user + \
               "\n    Password:    " + "*" * len(self.password) + \
               "\n    Query limit: " + str(self.limit)

    def validate(self):
        if self.url is None:
            return

        if self.user is None or self.password is None:
            raise InvalidConfigurationException("If database url is filled credentials should also be specified")
