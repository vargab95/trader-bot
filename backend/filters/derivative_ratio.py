#!/usr/bin/python3

import filters.base


class DerivativeRatio(filters.base.Filter):
    def put(self, value: float):
        self._data.append(value)
        if len(self._data) >= self._config.length:
            self._value = (self._data[-1] - self._data[0]) / self._data[-1]
            self._data.pop(0)
