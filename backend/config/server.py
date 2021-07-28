#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class ServerConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.port: int = config.get("port", 5000)
        self.datetime_format: str = config.get("datetime_format", '%Y-%m-%dT%H:%M:%S.%fZ')
        self.secret_key: str = config.get('secret_key', None)

    def validate(self):
        pass
