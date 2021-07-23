#!/usr/bin/python3

from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from filters.base import Filter


class FilterEventListener(Subscriber):
    def __init__(self, output_signal_id: str, filter_instance: Filter, publisher: Publisher):
        self.__value: float = None
        self.__filter: Filter = filter_instance
        self.__publisher: Publisher = publisher
        self.__output_signal_id = output_signal_id

    def update(self, event: SignalUpdatedEvent):
        self.__filter.put(event.value)
        self.__value = self.__filter.get()

        update_signal = SignalUpdatedEvent(self.__output_signal_id, self.__value)
        self.__publisher.notify_all_subscribers(update_signal)

    def read(self) -> float:
        return self.__value
