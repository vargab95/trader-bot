#!/usr/bin/python3

from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from fetcher.interface import Fetcher


class FetcherSignalPublisher(Subscriber):
    def __init__(self, output_signal_id: str, fetcher: Fetcher, publisher: Publisher):
        self.__value: float = None
        self.__fetcher: Fetcher = fetcher
        self.__publisher: Publisher = publisher
        self.__output_signal_id = output_signal_id

    def update(self, event: SignalUpdatedEvent):
        self.__fetcher.fetch_technical_indicator()
        self.__value = self.__fetcher.get_technical_indicator()

        update_signal = SignalUpdatedEvent(self.__output_signal_id, self.__value)
        self.__publisher.notify_all_subscribers(update_signal)

    def read(self) -> float:
        return self.__value
