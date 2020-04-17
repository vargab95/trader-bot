#!/usr/bin/python3

import typing

import filters.base


class NoFilterSpecified(Exception):
    pass


class Complex(filters.base.Filter):
    def __init__(self):
        super().__init__(0)

        self.__filters: typing.List[filters.base.Filter] = []
        self.__result = None

    def add_filter(self, new_filter: filters.base.Filter):
        self.__filters.append(new_filter)

    def put(self, value: float):
        value_to_use = value
        for filt in self.__filters:
            if value_to_use is not None:
                filt.put(value_to_use)
            value_to_use = filt.get()

    def get(self) -> float:
        try:
            return self.__filters[-1].get()
        except IndexError:
            raise NoFilterSpecified

    @property
    def length(self):
        return sum([filt.length for filt in self.__filters])

    @property
    def all(self) -> typing.List[float]:
        return None