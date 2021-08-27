#!/usr/bin/python3

import filters.base

from config.filter import FilterConfig


class SMA(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)

        self.__sum = 0.0

    def put(self, value: float):
        self._data.append(value)
        self.__sum += value
        if len(self._data) >= self._config.length:
            self._value = self.__sum / self._config.length
            self.__sum -= self._data.pop(0)
