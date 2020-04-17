#!/usr/bin/python3

import filters.base


class WMA(filters.base.Filter):
    def __init__(self, length):
        super().__init__(length)

        denominator = self.__get_nth_triangular_number(length)
        self.__coefficients = [i / denominator for i in range(1, length + 1)]

    @staticmethod
    def __get_nth_triangular_number(nth):
        return int(nth * (nth + 1) / 2)

    def put(self, value: float):
        self._data.append(value)
        if len(self._data) >= self._length:
            self._value = sum([
                self.__coefficients[i] * self._data[i]
                for i in range(self._length)
            ])
            self._data.pop(0)
