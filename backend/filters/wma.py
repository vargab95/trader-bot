#!/usr/bin/python3

import typing

import filters.base


class WMA(filters.base.Filter):
    def __init__(self, length):
        self.__length = length
        self.__data = []
        self.__sma = None

        denominator = self.__get_nth_triangular_number(length)
        self.__coefficients = [i / denominator for i in range(1, length + 1)]

    @staticmethod
    def __get_nth_triangular_number(nth):
        return int(nth * (nth + 1) / 2)

    def put(self, value: float):
        self.__data.append(value)
        if len(self.__data) >= self.__length:
            self.__sma = sum([
                self.__coefficients[i] * self.__data[i]
                for i in range(self.__length)
            ])
            self.__data.pop(0)

    def get(self) -> float:
        return self.__sma

    @property
    def length(self):
        return len(self.__data)

    @property
    def all(self) -> typing.List[float]:
        return self.__data
