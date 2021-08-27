#!/usr/bin/python3

import filters.base
import filters.ema

from config.filter import FilterConfig


class MACD(filters.base.Filter):
    def __init__(self, config: FilterConfig):
        super().__init__(config)

        self.__slower_ema = filters.ema.EMA(FilterConfig({"length": config.second_length}))
        self.__faster_ema = filters.ema.EMA(FilterConfig({"length": config.length}))
        self._value = None

    def put(self, value: float):
        self.__slower_ema.put(value)
        self.__faster_ema.put(value)

        slower_value = self.__slower_ema.get()
        faster_value = self.__faster_ema.get()
        if slower_value and faster_value:
            self._value = faster_value - slower_value

    @property
    def length(self):
        return self.__slower_ema.length  # pragma: no cover
