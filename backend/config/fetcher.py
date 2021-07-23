#!/usr/bin/python3

import typing

from exchange.interface import Market


class FetcherConfig:
    def __init__(self, config: typing.Dict):
        self.output_signal_id: str = config.get("output_signal_id", None)
        self.indicator_name: str = config.get("indicator_name", None)
        self.market: Market = Market.create_from_string(config.get("market", None))
        self.check_interval: int = int(config.get("check_interval", None))
        self.candle_size: str = config.get("candle_size", None)
