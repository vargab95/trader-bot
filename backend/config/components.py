#!/usr/bin/python3

import typing

from config.exchange import ExchangeConfig
from config.fetcher import FetcherConfig
from config.filter import FilterConfig
from config.detector import DetectorConfig, DetectorCombinationConfig
from config.trader import TraderConfig


class ComponentsConfig:
    def __init__(self, config: typing.Dict = None):
        self.exchanges = [ExchangeConfig(exchange_config) for exchange_config in config.get("exchanges", [])]
        self.fetchers = [FetcherConfig(fetcher_config) for fetcher_config in config.get("fetchers", [])]
        self.detectors = [DetectorConfig(detector_config) for detector_config in config.get("detectors", [])]
        self.detector_combinations = [DetectorCombinationConfig(detector_combination_config)
                                      for detector_combination_config
                                      in config.get("detector_combinations", [])]
        self.filters = [FilterConfig(filter_element) for filter_element in config.get("filters", [])]
        self.traders = [TraderConfig(trader_config) for trader_config in config.get("traders", {})]
