#!/usr/bin/python3

import filters.base
import filters.sma

from config.filter import FilterConfig


class EMA(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)
        self.__sma = filters.sma.SMA(FilterConfig({"length": config.length * 2}))

    def put(self, value: float):
        self._data.append(value)
        self.__sma.put(value)
        if len(self._data) >= 2 * self._config.length:
            alfa = 2.0 / (self._config.length + 1)
            current_ema = self.__sma.get()
            for i in self._data:
                current_ema = (alfa * i) + ((1 - alfa) * current_ema)
            self._value = current_ema
            self._data.pop(0)
            return current_ema
        return None

    @property
    def length(self):
        return self._config.length  # pragma: no cover
