#!/usr/bin/python3

import typing

import exchange.interface


class ExchangeConfig:
    available_exchanges = ["ftx", "binance"]

    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "binance")
        self.public_key = config.get("public_key", "")
        self.private_key = config.get("private_key", "")
        self.market_name_format = config.get("market_name_format", "{target}-{base}")

    def __str__(self):
        return "\nExchange:" + \
               "\n    Name:                  " + self.name + \
               "\n    Public key:            " + self.public_key + \
               "\n    Private key:           " + "*" * len(self.private_key) + \
               "\n    Market name format:    " + str(self.market_name_format)
