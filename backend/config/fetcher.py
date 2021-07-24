#!/usr/bin/python3

import typing

from exchange.interface import Market
from config.base import ConfigComponentBase


class FetcherConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.output_signal_id: str = config.get("output_signal_id", None)
        self.indicator_name: str = config.get("indicator_name", None)
        self.future: bool = config.get("future", False)
        self.market: Market = Market.create_from_string(config.get("market", None))
        self.check_interval: int = int(config.get("check_interval", None))
        self.candle_size: str = config.get("candle_size", None)
        self.exchange_id: str = config.get("exchange_id", None)
        self.type: str = config.get("type", "exchange")
