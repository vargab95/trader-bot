#!/usr/bin/python3

import typing

from config.logging import LoggingConfig
from config.testing import TestingConfig
from config.market import MarketConfig
from config.exchange import ExchangeConfig

class TraderConfig:
    def __init__(self, configuration: typing.Dict = {}):
        self.logging = LoggingConfig(configuration.get("logging", {}))
        self.testing = TestingConfig(configuration.get("testing", {}))
        self.market = MarketConfig(configuration.get("market", {}))
        self.exchange = ExchangeConfig(configuration.get("exchange", {}))
        self.follower_detector: bool = configuration.get("follower_mode", False)

    def __str__(self):
        return ''.join([str(attribute) for attribute in self.__dict__.values()])

