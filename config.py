#!/usr/bin/python3

import sys
import json
import yaml

class ExchangeConfig:
    def __init__(self):
        self.public_key: str = ""
        self.private_key: str = ""

    def __str__(self):
        return "\nExchange:" + \
               "\n    Public key:  " + self.public_key + \
               "\n    Private key: " + "*" * len(self.private_key)

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
        self.log_level: int = 0
        self.market: MarketConfig = MarketConfig()
        self.exchange: ExchangeConfig = ExchangeConfig()

    def __str__(self):
        return "\nGlobal:" + \
               "\n    Log level: " + str(self.log_level) + \
               str(self.market) + str(self.exchange)

class ConfigurationParser:
    def __init__(self):
        self.configuration = TraderConfig()

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            self.configuration.log_level = configuration["global"]["log_level"]
            self.configuration.market.name = configuration["market"]["name"]
            self.configuration.market.check_interval = configuration["market"]["check_interval"]
            self.configuration.market.candle_size = configuration["market"]["candle_size"]
            self.configuration.exchange.public_key = configuration["exchange"]["api_key"]
            self.configuration.exchange.private_key = configuration["exchange"]["api_secret"]
