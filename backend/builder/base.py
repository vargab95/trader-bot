#!/usr/bin/python3

import typing

from config.components import ComponentsConfig
from config.exchange import ExchangeConfig
from config.fetcher import FetcherConfig
from config.detector import DetectorConfig, DetectorCombinationConfig
from config.trader import TraderConfig
from observer.publisher import Publisher
from exchange.interface import ExchangeInterface
from exchange.factory import ExchangeControllerFactory
from fetcher.interface import Fetcher
from fetcher.factory import FetcherFactory
from fetcher.publisher import FetcherSignalPublisher
from filters.base import Filter
from filters.factory import FilterFactory
from filters.event_listener import FilterEventListener
from detector.interface import DetectorInterface
from detector.event_listener import DetectorEventListener
from detector.combination.base import DetectorCombinationLogic
from detector.combination.event_listener import DetectorCombinationEventListener
from detector.combination.factory import DetectorCombinationFactory
from detector.factory import DetectorFactory
from trader.base import TraderBase
from trader.factory import TraderFactory
from trader.event_listener import TradingActionListener


class TradingComponentsBuilderBase:
    def __init__(self):
        self.analogue_signal_publisher: Publisher = Publisher(name="Filtered signal")
        self.detector_signal_publisher: Publisher = Publisher(name="Detector signal")

        self.exchanges: typing.Dict[str, ExchangeInterface] = dict()
        self.fetchers: typing.Dict[str, Fetcher] = dict()
        self.fetcher_publishers: typing.Dict[str, Fetcher] = dict()
        self.filters: typing.Dict[str, Filter] = dict()
        self.filter_listeners: typing.Dict[str, FilterEventListener] = dict()
        self.detectors: typing.Dict[str, DetectorInterface] = dict()
        self.detector_listeners: typing.Dict[str, DetectorEventListener] = dict()
        self.detector_combinations: typing.Dict[str, DetectorCombinationLogic] = dict()
        self.detector_combination_listeners: typing.Dict[str, DetectorCombinationEventListener] = dict()
        self.traders: typing.Dict[str, TraderBase] = dict()
        self.trader_listeners: typing.Dict[str, TradingActionListener] = dict()

    def build(self, config: ComponentsConfig, testing: bool = False):
        self.create_exchanges(config.exchanges, testing)
        self.create_fetchers(config.fetchers)
        self.create_filters(config.filters)
        self.create_detectors(config.detectors)
        self.create_detector_combinations(config.detector_combinations)
        self.create_traders(config.traders)

    def create_exchanges(self, exchange_configs: typing.List[ExchangeConfig], testing: bool = False):
        for exchange_config in exchange_configs:
            self.exchanges[exchange_config.id] = ExchangeControllerFactory.create(exchange_config, testing)

    def create_fetchers(self, fetcher_configs: typing.List[FetcherConfig]):
        for fetcher_config in fetcher_configs:
            exchange = None
            if fetcher_config.type == "exchange":
                exchange = self.exchanges[fetcher_config.exchange_id]
            fetcher = FetcherFactory.create(fetcher_config, exchange)
            publisher = FetcherSignalPublisher(fetcher_config,
                                               fetcher,
                                               self.analogue_signal_publisher)

            self.fetchers[fetcher_config.output_signal_id] = fetcher
            self.fetcher_publishers[fetcher_config.output_signal_id] = publisher

            self.analogue_signal_publisher.register_signal(fetcher_config.output_signal_id)

    def create_filters(self, filter_configs: typing.List[FetcherConfig]):
        for filter_config in filter_configs:
            filter_instance = FilterFactory.create(filter_config)
            filter_listener = FilterEventListener(filter_config.output_signal_id,
                                                  filter_instance,
                                                  self.analogue_signal_publisher)

            self.analogue_signal_publisher.subscribe(filter_config.input_signal_id, filter_listener)
            self.filters[filter_config.output_signal_id] = filter_instance
            self.filter_listeners[filter_config.output_signal_id] = filter_listener

            self.analogue_signal_publisher.register_signal(filter_config.output_signal_id)

    def create_detectors(self, detector_configs: typing.List[DetectorConfig]):
        for detector_config in detector_configs:
            detector = DetectorFactory.create(detector_config)
            detector_listener = DetectorEventListener(detector_config.output_signal_id,
                                                      detector,
                                                      self.detector_signal_publisher)
            self.analogue_signal_publisher.subscribe(detector_config.input_signal_id, detector_listener)
            self.detectors[detector_config.output_signal_id] = detector
            self.detector_listeners[detector_config.output_signal_id] = detector_listener

            self.detector_signal_publisher.register_signal(detector_config.output_signal_id)

    def create_detector_combinations(self, detector_combination_configs: typing.List[DetectorCombinationConfig]):
        for detector_combination_config in detector_combination_configs:
            detector_combination = DetectorCombinationFactory.create(detector_combination_config)
            listener = DetectorCombinationEventListener(detector_combination_config.output_signal_id,
                                                        detector_combination,
                                                        self.detector_signal_publisher)
            for input_signal_id in detector_combination_config.input_signal_ids:
                self.detector_signal_publisher.subscribe(input_signal_id, listener)
            self.detector_combinations[detector_combination_config.output_signal_id] = detector_combination
            self.detector_combination_listeners[detector_combination_config.output_signal_id] = listener

            self.detector_signal_publisher.register_signal(detector_combination_config.output_signal_id)

    def create_traders(self, trader_configs: typing.List[TraderConfig]):
        for trader_config in trader_configs:
            trader = TraderFactory.create(trader_config, self.exchanges[trader_config.exchange])
            listener = TradingActionListener()
            self.detector_signal_publisher.subscribe(trader_config.input_signal_id, listener)
            self.traders[trader_config.input_signal_id] = trader
            self.trader_listeners[trader_config.input_signal_id] = listener
