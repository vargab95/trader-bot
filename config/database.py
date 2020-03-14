#!/usr/bin/python3

import typing


class DatabaseConfig:
    def __init__(self, config: typing.Dict):
        self.url = config.get("url", "")
        self.user = config.get("user", "")
        self.password = config.get("password", "")

    def __str__(self):
        return "\nDatabase:" + \
               "\n    URL:      " + self.url + \
               "\n    Username: " + self.user + \
               "\n    Password: " + "*" * len(self.password)
