#!/usr/bin/python3

import abc

from observer.event import SignalUpdatedEvent


class Subscriber(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, event: SignalUpdatedEvent):  # pragma: no cover
        pass
