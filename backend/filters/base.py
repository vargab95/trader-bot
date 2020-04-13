#!/usr/bin/python3

import abc
import typing


class Filter:
    @abc.abstractmethod
    def put(self, value: float):
        pass

    @abc.abstractmethod
    def get(self) -> float:
        pass

    @abc.abstractproperty
    def length(self):
        pass

    @abc.abstractproperty
    def all(self) -> typing.List[float]:
        pass
