#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class ExchangeConfig(ConfigComponentBase):
    available_exchanges = ["ftx", "binance"]

    def __init__(self, config: typing.Dict):
        # Id of the exchange. Custom string which can be used later to identify the exchange
        self.id = config.get("id", None)

        # Name of the exchange to be used. For available options, please check available_exchanges
        # class variable
        self.name = config.get("name", None)

        # Public key, generated on the exchange
        self.public_key = config.get("public_key", None)

        # Private key, generated on the exchange
        self.private_key = config.get("private_key", None)

        # As market name formats can vary between exchanges, it's necessary to specify it.
        # For example, if BTC-USDT is used in the exchange, {target}-{base} must be specified
        self.market_name_format = config.get("market_name_format", "{target}-{base}")

        # Testing mode options
        self.start_money = config.get("start_money", 100.0)
        self.base_asset = config.get("base_asset", "USDT")

        # Real time flag means, the simulator application will fetch the data from an exchange
        # and won't provide test data even in testing mode
        self.real_time = config.get("real_time", True)

        # Fee for the test. It should be filled based on the documentation of the exchange
        self.fee = config.get("fee", 0.0)

        # Precision of balance calculation. It can differ between exchanges
        self.balance_precision = config.get("balance_precision", 0.00000001)
        self.leverage = config.get("leverage", 1.0)

    def validate(self):
        if self.id is None:
            raise InvalidConfigurationException("Id is a mandatory parameter for exchange config")

        if self.name is None:
            raise InvalidConfigurationException("Name is a mandatory parameter for exchange config")

        if self.name not in self.available_exchanges:
            raise InvalidConfigurationException("Name is invalid")

        if self.public_key is None:
            raise InvalidConfigurationException("Public key is a mandatory parameter for exchange config")

        if self.private_key is None:
            raise InvalidConfigurationException("Private key is a mandatory parameter for exchange config")

    def dict(self):
        result = super().dict()
        result["private_key"] = "*" * 10
        return result
