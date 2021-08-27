#!/usr/bin/python3

import filters.base

from config.filter import FilterConfig


class NthFilter(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)

        self.__number_of_values: int = 0

    def put(self, value: float):
        self.__number_of_values += 1
        if self.__number_of_values >= self._config.length:
            self._value = value
            self.__number_of_values = 0
