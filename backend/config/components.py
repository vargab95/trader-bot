#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.exchange import ExchangeConfig
from config.fetcher import FetcherConfig
from config.filter import FilterConfig
from config.detector import DetectorConfig, DetectorCombinationConfig
from config.trader import TraderConfig
from config.common import InvalidConfigurationException


class ComponentsConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict = None):
        self.exchanges = [ExchangeConfig(exchange_config) for exchange_config in config.get("exchanges", [])]
        self.fetchers = [FetcherConfig(fetcher_config) for fetcher_config in config.get("fetchers", [])]
        self.detectors = [DetectorConfig(detector_config) for detector_config in config.get("detectors", [])]
        self.detector_combinations = [DetectorCombinationConfig(detector_combination_config)
                                      for detector_combination_config
                                      in config.get("detector_combinations", [])]
        self.filters = [FilterConfig(filter_element) for filter_element in config.get("filters", [])]
        self.traders = [TraderConfig(trader_config) for trader_config in config.get("traders", {})]

    def validate(self):
        for attribute in self.__dict__.values():
            for i in attribute:
                i.validate()

        fetcher_signals = [fc.output_signal_id for fc in self.fetchers]
        filter_signals = [fc.output_signal_id for fc in self.filters]
        detector_signals = [dc.output_signal_id for dc in self.detectors]
        detector_combination_signals = [dc.output_signal_id for dc in self.detector_combinations]

        for filter_config in self.filters:
            if filter_config.input_signal_id not in fetcher_signals:
                raise InvalidConfigurationException("No provided signal for filter input"
                                                    f"{filter_config.input_signal_id}")

        for detector_config in self.detectors:
            if detector_config.input_signal_id not in filter_signals:
                raise InvalidConfigurationException("No provided signal for detector input"
                                                    f"{detector_config.input_signal_id}")

        for detector_combination_config in self.detector_combinations:
            for input_signal_id in detector_combination_config.input_signal_ids:
                if input_signal_id not in detector_signals:
                    raise InvalidConfigurationException("No provided signal for detector combination input"
                                                        f"{input_signal_id}")

        for trader_config in self.traders:
            if trader_config.input_signal_id not in detector_signals and \
                    trader_config.input_signal_id not in detector_combination_signals:
                raise InvalidConfigurationException("No provided signal for trader input"
                                                    f"{trader_config.input_signal_id}")
