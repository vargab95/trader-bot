#!/usr/bin/python3

import logging
from datetime import datetime

from observer.publisher import Publisher
from observer.event import SignalUpdatedEvent

from config.fetcher import FetcherConfig
from signals.trading_signal import TickerSignalDescriptor
from fetcher.interface import Fetcher


class FetcherSignalPublisher:
    def __init__(self, configuration: FetcherConfig, fetcher: Fetcher, publisher: Publisher):
        self.__value: float = None
        self.__fetcher: Fetcher = fetcher
        self.__publisher: Publisher = publisher
        self.__config: FetcherConfig = configuration
        self.__initial_burst_done = False

    def publish(self):
        if not self.__initial_burst_done:
            self.__publish_initial_values()
            self.__initial_burst_done = True

        self.__fetcher.fetch_technical_indicator()
        self.__value = self.__fetcher.get_technical_indicator()

        update_signal = SignalUpdatedEvent(self.__config.output_signal_id, self.__value)
        self.__publisher.notify_all_subscribers(update_signal)

    def __publish_initial_values(self):
        history = None
        if self.__config.initial_values:
            history = self.__config.initial_values
        elif self.__config.initial_length > 0:
            history = self.__get_initial_values_from_exchange()
        logging.info("Publishing the following list as initial value list: %s", str(history))
        if history:
            for signal_point in history:
                self.__value = signal_point.value
                update_signal = SignalUpdatedEvent(self.__config.output_signal_id, self.__value)
                self.__publisher.notify_all_subscribers(update_signal)

    def __get_initial_values_from_exchange(self):
        limit = self.__config.initial_length * self.__config.initial_step
        start_date = datetime.utcnow() - self.__config.initial_resolution * limit
        descriptor = TickerSignalDescriptor(market=self.__config.market,
                                            limit=limit,
                                            resolution=self.__config.initial_resolution,
                                            start_date=start_date,
                                            keyword=self.__config.initial_keyword)
        history = self.__fetcher.get_indicator_history(descriptor)
        return history.data[::self.__config.initial_step]

    def read(self) -> float:
        return self.__value
