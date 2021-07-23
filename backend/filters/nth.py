#!/usr/bin/python3

import filters.base


class NthFilter(filters.base.Filter):
    def __init__(self, length):
        super().__init__(length)

        self.__number_of_values: int = 0

    def put(self, value: float):
        self.__number_of_values += 1
        if self.__number_of_values >= self._length:
            self._value = value
            self.__number_of_values = 0
