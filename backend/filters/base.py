#!/usr/bin/python3

import abc

from config.filter import FilterConfig


class Filter:
    def __init__(self, config: FilterConfig):
        self._config = config
        self._data = []
        self._value = None

    @abc.abstractmethod
    def put(self, value: float):
        pass  # pragma: no cover

    def get(self) -> float:
        return self._value

    @property
    def length(self):
        return self._config.length
