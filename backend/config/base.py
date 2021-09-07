#!/usr/bin/python3

from datetime import timedelta

from exchange.interface import Market
from trader.common import TraderState


class ConfigComponentBase:
    def validate(self):
        for attribute in self.__dict__.values():
            attribute.validate()

    def dict(self):
        result = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigComponentBase):
                result[key] = value.dict()
            elif isinstance(value, Market):
                result[key] = str(value)
            elif isinstance(value, timedelta):
                result[key] = str(value)
            elif isinstance(value, TraderState):
                result[key] = str(value)
            else:
                result[key] = value
        return result
