#!/usr/bin/python3

from datetime import datetime, timedelta

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
            history = None
            if self.__config.initial_values:
                history = self.__config.initial_values
            elif self.__config.initial_length > 0:
                limit = self.__config.initial_length * self.__config.initial_step
                start_date = datetime.now() - self.__config.initial_resolution * limit
                descriptor = TickerSignalDescriptor(market=self.__config.market,
                                                    limit=limit,
                                                    resolution=self.__config.initial_resolution,
                                                    start_date=start_date,
                                                    keyword=self.__config.initial_keyword)
                history = self.__fetcher.get_indicator_history(descriptor)
                history = history.data[::self.__config.initial_step]

            if history:
                for signal_point in history:
                    self.__value = signal_point.value
                    update_signal = SignalUpdatedEvent(self.__config.output_signal_id, self.__value)
                    self.__publisher.notify_all_subscribers(update_signal)

            self.__initial_burst_done = True

        self.__fetcher.fetch_technical_indicator()
        self.__value = self.__fetcher.get_technical_indicator()

        update_signal = SignalUpdatedEvent(self.__config.output_signal_id, self.__value)
        self.__publisher.notify_all_subscribers(update_signal)

    def read(self) -> float:
        return self.__value
