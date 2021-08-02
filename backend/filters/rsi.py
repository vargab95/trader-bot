#!/usr/bin/python3

import math
import numpy
import talib

import filters.base


class RSI(filters.base.Filter):
    def put(self, value: float):
        self._data.append(float(value))

        result_list = list(talib.RSI(numpy.array(self._data), timeperiod=self.length))
        result = result_list[-1]
        self._value = None if math.isnan(result) else result
