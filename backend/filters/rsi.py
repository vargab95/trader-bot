#!/usr/bin/python3

import typing

from config.filter import FilterConfig

import filters.base


class RSI(filters.base.Filter):
    def __init__(self, configuration: FilterConfig):
        super().__init__(configuration)

        self.__gains: typing.List[float] = list()
        self.__losses: typing.List[float] = list()
        self.__prev_avg_gain: float = None
        self.__prev_avg_loss: float = None

    def put(self, value: float):
        self._data.append(float(value))
        if len(self._data) > 2:
            self._data.pop(0)
        elif len(self._data) <= 1:
            return

        difference = self._data[-1] - self._data[-2]
        if difference > 0:
            gain = difference
            loss = 0
        elif difference < 0:
            gain = 0
            loss = abs(difference)
        else:
            gain = 0
            loss = 0

        self.__gains.append(gain)
        self.__losses.append(loss)

        if len(self.__gains) < self._config.length:
            return

        if len(self.__gains) > self._config.length:
            self.__gains.pop(0)
            self.__losses.pop(0)

        # Calculate SMA for first gain
        if self.__prev_avg_gain is None:
            avg_gain = sum(self.__gains) / len(self.__gains)
            avg_loss = sum(self.__losses) / len(self.__losses)
        # Use WSM after initial window-length period
        else:
            avg_gain = (self.__prev_avg_gain * (self._config.length - 1) + gain) / self._config.length
            avg_loss = (self.__prev_avg_loss * (self._config.length - 1) + loss) / self._config.length

        self.__prev_avg_gain = avg_gain
        self.__prev_avg_loss = avg_loss

        try:
            self._value = 100 - (100 / (1 + avg_gain / avg_loss))
        except ZeroDivisionError:
            self._value = None
