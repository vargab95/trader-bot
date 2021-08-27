#!/usr/bin/python3

import filters.base

from config.filter import FilterConfig


class WMA(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)

        denominator = self.__get_nth_triangular_number(config.length)
        self.__coefficients = [i / denominator for i in range(1, config.length + 1)]

    @staticmethod
    def __get_nth_triangular_number(nth):
        return int(nth * (nth + 1) / 2)

    def put(self, value: float):
        self._data.append(value)
        if len(self._data) >= self._config.length:
            self._value = sum([
                self.__coefficients[i] * self._data[i]
                for i in range(self._config.length)
            ])
            self._data.pop(0)
