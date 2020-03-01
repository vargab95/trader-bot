#!/usr/bin/python3

import sys
import json
import yaml

import typing
import exchange.interface

class LoggingConfig:
    def __init__(self, config: typing.Dict):
        self.level: int = config.get("level", 31)
        self.path: str = config.get("path", "")

    def __str__(self):
        return "\nLogging:" + \
               "\n    Level: " + str(self.level) + \
               "\n    Path:  " + str(self.path)

class TestingConfig:
    def __init__(self, config: typing.Dict):
        self.enabled: bool = config.get("enabled", False)
        self.real_time: bool = config.get("real_time", False)
        self.start_money: float = config.get("start_money", 100.0)

    def __str__(self):
        return "\nTesting:" + \
               "\n    Enabled:     " + str(self.enabled) + \
               "\n    Real time:   " + str(self.real_time) + \
               "\n    Start money: " + str(self.start_money)

class ExchangeConfig:
    def __init__(self, config: typing.Dict):
        self.public_key = config.get("api_key", "")
        self.private_key = config.get("api_secret", "")
        self.watched_market: exchange.interface.Market = \
                exchange.interface.Market.create_from_string(config.get("watched_market", "BTC-USDT"))
        self.bearish_market: exchange.interface.Market = \
                exchange.interface.Market.create_from_string(config.get("bearish_market", "BEAR-USDT"))
        self.bullish_market: exchange.interface.Market = \
                exchange.interface.Market.create_from_string(config.get("bullish_market", "BULL-USDT"))

    def __str__(self):
        return "\nExchange:" + \
               "\n    Public key:          " + self.public_key + \
               "\n    Private key:         " + "*" * len(self.private_key) + \
               "\n    Watched market name: " + str(self.watched_market) + \
               "\n    Bullish market name: " + str(self.bullish_market) + \
               "\n    Bearish market name: " + str(self.bearish_market)

class MarketConfig:
    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "GEMINI:BTCUSD")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.bullish_threshold = config.get("bullish_threshold", 0.0)
        self.bearish_threshold = config.get("bullish_threshold", 0.0)

    def __str__(self):
        return "\nMarket:" + \
               "\n    Name:              " + self.name + \
               "\n    Candle size:       " + self.candle_size + \
               "\n    Check interval:    " + str(self.check_interval) + \
               "\n    Bullish threshold: " + str(self.bullish_threshold) + \
               "\n    Bearish threshold: " + str(self.bearish_threshold)

class TraderConfig:
    def __init__(self, configuration: typing.Dict = {}):
        self.logging = LoggingConfig(configuration.get("logging", {}))
        self.testing = TestingConfig(configuration.get("testing", {}))
        self.market = MarketConfig(configuration.get("market", {}))
        self.exchange = ExchangeConfig(configuration.get("exchange", {}))

    def __str__(self):
        return ''.join([str(attribute) for attribute in self.__dict__.values()])

class ConfigurationParser:
    def __init__(self):
        self.configuration: TraderConfig = None

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            self.configuration = TraderConfig(configuration)
