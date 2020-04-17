#!/usr/bin/python3

import filters.base


class Derivative(filters.base.Filter):
    def put(self, value: float):
        self._data.append(value)
        if len(self._data) >= self._length:
            self._value = self._data[-1] - self._data[0]
            self._data.pop(0)
