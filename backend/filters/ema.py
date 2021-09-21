#!/usr/bin/python3

import filters.base
import filters.sma

from config.filter import FilterConfig


class EMA(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)
        self.__sma = filters.sma.SMA(FilterConfig({"length": config.length}))

    def put(self, value: float):
        self._data.append(value)

        if self._value is None:
            self.__sma.put(value)
            self._value = self.__sma.get()

        if len(self._data) > self._config.length:
            alfa = round(2.0 / (self._config.length + 1), 4)
            self._value = alfa * (value - self._value) + self._value
            self._data.pop(0)

        return self._value

    @property
    def length(self):
        return self._config.length  # pragma: no cover
