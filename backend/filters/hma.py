#!/usr/bin/python3

import typing

import filters.base
import filters.wma


class HMA(filters.base.Filter):
    def __init__(self, length):
        self.__n_wma = filters.wma.WMA(length)
        self.__np2_wma = filters.wma.WMA(int(length / 2))
        self.__sqrt_wma = filters.wma.WMA(int(length**0.5))
        self.__hma = None

    def put(self, value: float):
        self.__n_wma.put(value)
        self.__np2_wma.put(value)

        n_value = self.__n_wma.get()
        np2_value = self.__np2_wma.get()
        if n_value and np2_value:
            self.__sqrt_wma.put(2 * np2_value - n_value)

        hma_value = self.__sqrt_wma.get()
        if hma_value:
            self.__hma = hma_value

    def get(self) -> float:
        return self.__hma

    @property
    def length(self):
        return self.__n_wma.length

    @property
    def all(self) -> typing.List[float]:
        pass