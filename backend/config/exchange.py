#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class ExchangeConfig(ConfigComponentBase):
    available_exchanges = ["ftx", "binance"]

    def __init__(self, config: typing.Dict):
        print("CFG", config)
        self.id = config.get("id", None)
        self.name = config.get("name", None)
        self.public_key = config.get("public_key", None)
        self.private_key = config.get("private_key", None)
        self.market_name_format = config.get("market_name_format", "{target}-{base}")

        # Testing mode options
        self.start_money = config.get("start_money", 100.0)
        self.base_asset = config.get("base_asset", "USDT")
        self.real_time = config.get("real_time", True)
        self.fee = config.get("fee", 0.0)
        self.balance_precision = config.get("balance_precision", 0.00000001)

    def validate(self):
        if self.id is None:
            raise InvalidConfigurationException("Id is a mandatory parameter for exchange config")

        if self.name is None:
            raise InvalidConfigurationException("Name is a mandatory parameter for exchange config")

        if self.public_key is None:
            raise InvalidConfigurationException("Public key is a mandatory parameter for exchange config")

        if self.private_key is None:
            raise InvalidConfigurationException("Private key is a mandatory parameter for exchange config")
