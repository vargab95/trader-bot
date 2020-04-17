#!/usr/bin/python3

import typing

import filters.base


class Derivative(filters.base.Filter):
    def __init__(self, length):
        self.__length = length
        self.__data = []
        self.__derivative = None

    def put(self, value: float):
        self.__data.append(value)
        if len(self.__data) >= self.__length:
            self.__derivative = self.__data[-1] - self.__data[0]
            self.__data.pop(0)

    def get(self) -> float:
        return self.__derivative

    @property
    def length(self):
        return len(self.__data)

    @property
    def all(self) -> typing.List[float]:
        return self.__data
