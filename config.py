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
        self.watched_market: str = ""
        self.bullish_market: str = ""
        self.bearish_market: str = ""

    def __str__(self):
        return "\nExchange:" + \
               "\n    Public key:          " + self.public_key + \
               "\n    Private key:         " + "*" * len(self.private_key) + \
               "\n    Watched market name: " + self.watched_market + \
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

            logging_config = configuration.get("logging", {})
            self.configuration.logging.level = logging_config.get("level", 31)
            self.configuration.logging.path = logging_config.get("path", "")

            testing_config = configuration.get("testing", {})
            self.configuration.testing.enabled = testing_config.get("enabled", False)
            self.configuration.testing.start_money = testing_config.get("start_money", 100.0)

            market_config = configuration.get("market", {})
            self.configuration.market.name = market_config.get("name", "GEMINI:BTCUSD")
            self.configuration.market.check_interval = market_config.get("check_interval", 60)
            self.configuration.market.candle_size = market_config.get("candle_size", "1h")

            exchange_config = configuration.get("exchange", {})
            self.configuration.exchange.public_key = exchange_config.get("api_key", "")
            self.configuration.exchange.private_key = exchange_config.get("api_secret", "")
            self.configuration.exchange.watched_market = exchange_config.get("watched_market", "BTCUSDT")
            self.configuration.exchange.bearish_market = exchange_config.get("bearish_market", "BEARUSDT")
            self.configuration.exchange.bull_market = exchange_config.get("bullish_market", "BULLUSDT")
