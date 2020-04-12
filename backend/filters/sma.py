#!/usr/bin/python3

import filters.base


class SMA(filters.base.Filter):
    def __init__(self, length):
        self.__length = length
        self.__data = []
        self.__sum = 0.0
        self.__sma = None

    def put(self, value: float):
        self.__data.append(value)
        self.__sum += value
        if len(self.__data) >= self.__length:
            self.__sma = self.__sum / self.__length
            self.__sum -= self.__data.pop(0)

    def get(self) -> float:
        return self.__sma

    @property
    def length(self):
        return len(self.__data)
