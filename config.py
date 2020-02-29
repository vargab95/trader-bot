#!/usr/bin/python3

import sys
import json
import yaml

class LoggingConfig:
    def __init__(self):
        self.level: int = 10
        self.path: str = ""

    def __str__(self):
        return "\nLogging:" + \
               "\n    Level: " + str(self.level) + \
               "\n    Path:  " + str(self.path)

class TestingConfig:
    def __init__(self):
        self.enabled: bool = False
        self.start_money: float = 0.0

    def __str__(self):
        return "\nTesting:" + \
               "\n    Enabled:     " + str(self.enabled) + \
               "\n    Start money: " + str(self.start_money)

class ExchangeConfig:
    def __init__(self):
        self.public_key: str = ""
        self.private_key: str = ""
        self.bullish_market: str = ""
        self.bearish_market: str = ""

    def __str__(self):
        return "\nExchange:" + \
               "\n    Public key:          " + self.public_key + \
               "\n    Private key:         " + "*" * len(self.private_key) + \
               "\n    Bullish market name: " + self.bullish_market + \
               "\n    Bearish market name: " + self.bearish_market

class MarketConfig:
    def __init__(self):
        self.name: str = ""
        self.candle_size: str = ""
        self.check_interval: int = 0

    def __str__(self):
        return "\nMarket:" + \
               "\n    Name:           " + self.name + \
               "\n    Candle size:    " + self.candle_size + \
               "\n    Check interval: " + str(self.check_interval)

class TraderConfig:
    def __init__(self):
        self.logging: LoggingConfig = LoggingConfig()
        self.market: MarketConfig = MarketConfig()
        self.exchange: ExchangeConfig = ExchangeConfig()
        self.testing: TestingConfig = TestingConfig()

    def __str__(self):
        return str(self.logging) + str(self.market) + \
               str(self.exchange) + str(self.testing)

class ConfigurationParser:
    def __init__(self):
        self.configuration = TraderConfig()

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)

            self.configuration.logging.level = configuration["logging"]["level"]
            self.configuration.logging.path = configuration["logging"]["path"]

            self.configuration.testing.enabled = configuration["testing"]["enabled"]
            self.configuration.testing.start_money = configuration["testing"]["start_money"]

            self.configuration.market.name = configuration["market"]["name"]
            self.configuration.market.check_interval = configuration["market"]["check_interval"]
            self.configuration.market.candle_size = configuration["market"]["candle_size"]

            self.configuration.exchange.public_key = configuration["exchange"]["api_key"]
            self.configuration.exchange.private_key = configuration["exchange"]["api_secret"]
