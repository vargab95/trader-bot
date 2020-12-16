#!/usr/bin/python3

import typing

import exchange.interface


class ExchangeConfig:
    available_exchanges = ["ftx", "binance"]

    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "binance")
        self.public_key = config.get("public_key", "")
        self.private_key = config.get("private_key", "")
        self.watched_market: exchange.interface.Market = \
            exchange.interface.Market.create_from_string(
                config.get("watched_market", "BTC-USDT"))
        self.bearish_market: exchange.interface.Market = \
            exchange.interface.Market.create_from_string(
                config.get("bearish_market", "BEAR-USDT"))
        self.bullish_market: exchange.interface.Market = \
            exchange.interface.Market.create_from_string(
                config.get("bullish_market", "BULL-USDT"))
        # TODO it may should be evaluated as an enum instead of simple string!
        self.default_price_keyword = config.get(
            "default_price_keyword", "price")
        self.bullish_price_keyword = config.get(
            "bullish_price_keyword", "price")
        self.bearish_price_keyword = config.get(
            "bearish_price_keyword", "price")
        self.market_name_format = config.get("market_name_format",
                                             "{target}-{base}")
        self.future = config.get("future", False)

    def __str__(self):
        return "\nExchange:" + \
               "\n    Name:                  " + self.name + \
               "\n    Public key:            " + self.public_key + \
               "\n    Private key:           " + "*" * len(self.private_key) + \
               "\n    Watched market name:   " + str(self.watched_market) + \
               "\n    Bullish market name:   " + str(self.bullish_market) + \
               "\n    Bearish market name:   " + str(self.bearish_market) + \
               "\n    Market name format:    " + str(self.market_name_format) + \
               "\n    Default price keyword: " + str(self.default_price_keyword) + \
               "\n    Bearish price keyword: " + str(self.bearish_price_keyword) + \
               "\n    Bullish price keyword: " + str(self.bullish_price_keyword) + \
               "\n    Future:                " + str(self.future)
