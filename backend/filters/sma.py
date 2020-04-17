#!/usr/bin/python3

import filters.base


class SMA(filters.base.Filter):
    def __init__(self, length):
        super().__init__(length)

        self.__sum = 0.0

    def put(self, value: float):
        self._data.append(value)
        self.__sum += value
        if len(self._data) >= self._length:
            self._value = self.__sum / self._length
            self.__sum -= self._data.pop(0)
