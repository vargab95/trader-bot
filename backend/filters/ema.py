#!/usr/bin/python3

import filters.base
import filters.wma

from config.filter import FilterConfig


class EMA(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)

        self.__n_wma = filters.wma.WMA(config)
        self.__np2_wma = filters.wma.WMA(FilterConfig({"length": int(config.length / 2)}))
        self.__sqrt_wma = filters.wma.WMA(FilterConfig({"length": int(config.length ** 0.5)}))
        self._value = None

    def put(self, value: float):
        self.__n_wma.put(value)
        self.__np2_wma.put(value)

        n_value = self.__n_wma.get()
        np2_value = self.__np2_wma.get()
        if n_value and np2_value:
            self.__sqrt_wma.put(2 * np2_value - n_value)

        hma_value = self.__sqrt_wma.get()
        if hma_value:
            self._value = hma_value

    @property
    def length(self):
        return self.__n_wma.length  # pragma: no cover
