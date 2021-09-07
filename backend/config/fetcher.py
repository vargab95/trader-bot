#!/usr/bin/python3

import typing
from datetime import timedelta

from exchange.interface import Market
from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class FetcherConfig(ConfigComponentBase):
    available_types = ["exchange", "trading_view", "csv_file"]

    def __init__(self, config: typing.Dict):
        self.output_signal_id: str = config.get("output_signal_id", None)
        self.indicator_name: str = config.get("indicator_name", None)
        self.future: bool = config.get("future", False)
        if isinstance(config.get("market"), list):
            self.market: Market = [Market.create_from_string(market) for market in config.get("market", None)]
        else:
            self.market: Market = Market.create_from_string(config.get("market", None))
        self.check_interval: int = int(config.get("check_interval", None))
        self.candle_size: str = config.get("candle_size", None)
        self.exchange_id: str = config.get("exchange_id", None)
        self.type: str = config.get("type", "exchange")
        self.indicator: str = config.get("indicator", "all")
        self.path: str = config.get("path", None)

        self.initial_values = config.get("initial_values", [])
        self.initial_length = config.get("initial_length", 0)
        self.initial_keyword = config.get("initial_keyword", "close")
        self.initial_step = config.get("initial_step", 1)
        self.initial_resolution = timedelta(seconds=config.get("initial_resolution", 3600))

    def validate(self):
        if self.output_signal_id is None:
            raise InvalidConfigurationException("Output signal id is a mandatory fetcher configuration option")

        if self.type == "trading_view" and self.indicator_name is None:
            raise InvalidConfigurationException("Indicator name is a mandatory fetcher configuration option")

        if self.market is None:
            raise InvalidConfigurationException("Market is a mandatory fetcher configuration option")

        if self.check_interval is None:
            raise InvalidConfigurationException("Check interval is a mandatory fetcher configuration option")

        if self.exchange_id is None:
            raise InvalidConfigurationException("Exchange id is a mandatory fetcher configuration option")

        if self.type not in self.available_types:
            raise InvalidConfigurationException(f"{self.type} is not a valid fetcher type")

        if self.type == "csv_file" and self.path is None:
            raise InvalidConfigurationException("path is mandatory for csv_file typed fetcher")
