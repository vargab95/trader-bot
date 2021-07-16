#!/usr/bin/python3

import typing
from dataclasses import dataclass


@dataclass
class ObserverEvent:
    signal_name: str


@dataclass
class SignalUpdatedEvent(ObserverEvent):
    value: typing.Union[int, float]
