#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class TestingConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.enabled: bool = config.get("enabled", False)
        self.base_asset: str = config.get("base_asset", "USDT")
        self.balance_precision: float = config.get("balance_precision", 0.0001)

    def validate(self):
        pass
