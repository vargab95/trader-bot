#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class TestingConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.enabled: bool = config.get("enabled", False)
        self.base_asset: str = config.get("base_asset", "USDT")
        self.balance_precision: float = config.get("balance_precision", 0.0001)

    def __str__(self):
        return "\nTesting:" + \
               "\n    Enabled:           " + str(self.enabled) + \
               "\n    Balance precision: " + str(self.balance_precision)

    def validate(self):
        pass
