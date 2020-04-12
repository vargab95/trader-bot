#!/usr/bin/python3

import typing


class ServerConfig:
    def __init__(self, config: typing.Dict):
        self.port: int = config.get("port", 5000)
        self.datetime_format: str = config.get("datetime_format",
                                               '%Y-%m-%dT%H:%M:%S.%fZ')

    def __str__(self):
        return "\nServer:" + \
               "\n    Port:             " + str(self.port) + \
               "\n    Date time format: " + self.datetime_format