#!/usr/bin/python3

import logging
import typing

from observer.subscriber import Subscriber
from observer.errors import SignalDoesNotExists, SubscriberCannotBeFound
from observer.event import ObserverEvent


class Publisher:
    def __init__(self, name: str = None):
        self.name: str = name
        self.__subscribers: typing.Dict[str, Subscriber] = dict()

    def subscribe(self, signal_id: str, subscriber: Subscriber) -> None:
        logging.info("%s subscribed for %s", str(subscriber), signal_id)
        try:
            self.__subscribers[signal_id].append(subscriber)
        except KeyError as exc:
            raise SignalDoesNotExists(f"There is no signal published with id {signal_id}") from exc

    def unsubscribe(self, signal_id: str, subscriber: Subscriber) -> None:
        logging.info("%s unsubscribed from %s", str(subscriber), signal_id)
        try:
            self.__subscribers[signal_id].remove(subscriber)
        except KeyError as exc:
            raise SignalDoesNotExists(f"There is no signal published with id {signal_id}") from exc
        except ValueError as exc:
            raise SubscriberCannotBeFound(f"Subscriber {subscriber} is not registered for signal {signal_id}") from exc

    def notify_all_subscribers(self, event: ObserverEvent) -> None:
        logging.info("%s was published", event.signal_name)
        try:
            for subscriber in self.__subscribers[event.signal_name]:
                subscriber.update(event)
        except KeyError as exc:
            raise SignalDoesNotExists(f"There is no signal published with id {event.signal_name}") from exc

    def register_signal(self, signal_id: str):
        self.__subscribers[signal_id] = list()
