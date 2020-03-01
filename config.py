#!/usr/bin/python3

import sys
import json
import yaml

import typing

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
        self.start_money: float = config.get("start_money", 100.0)

    def __str__(self):
        return "\nTesting:" + \
               "\n    Enabled:     " + str(self.enabled) + \
               "\n    Start money: " + str(self.start_money)

class ExchangeConfig:
    def __init__(self, config: typing.Dict):
        self.public_key = config.get("api_key", "")
        self.private_key = config.get("api_secret", "")
        self.watched_market = config.get("watched_market", "BTCUSDT")
        self.bearish_market = config.get("bearish_market", "BEARUSDT")
        self.bullish_market = config.get("bullish_market", "BULLUSDT")

    def __str__(self):
        return "\nExchange:" + \
               "\n    Public key:          " + self.public_key + \
               "\n    Private key:         " + "*" * len(self.private_key) + \
               "\n    Watched market name: " + self.watched_market + \
               "\n    Bullish market name: " + self.bullish_market + \
               "\n    Bearish market name: " + self.bearish_market

class MarketConfig:
    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "GEMINI:BTCUSD")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")

    def __str__(self):
        return "\nMarket:" + \
               "\n    Name:           " + self.name + \
               "\n    Candle size:    " + self.candle_size + \
               "\n    Check interval: " + str(self.check_interval)

class TraderConfig:
    def __init__(self):
        self.logging: LoggingConfig = None
        self.market: MarketConfig = None
        self.exchange: ExchangeConfig = None
        self.testing: TestingConfig = None

    def __str__(self):
        return ''.join([str(attribute) for attribute in self.__dict__.values()])

class ConfigurationParser:
    def __init__(self):
        self.configuration = TraderConfig()

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)

            self.configuration.logging = LoggingConfig(configuration.get("logging", {}))
            self.configuration.testing = TestingConfig(configuration.get("testing", {}))
            self.configuration.market = MarketConfig(configuration.get("market", {}))
            self.configuration.exchange = ExchangeConfig(configuration.get("exchange", {}))
