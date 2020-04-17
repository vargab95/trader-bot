#!/usr/bin/python3

import filters.sma
import filters.wma
import filters.hma


class InvalidFilterFactoryParameter(Exception):
    pass


class FilterFactory:
    available_types = ["sma", "wma", "hma", "derivative"]

    @staticmethod
    def create(filter_type: str, length: int = 2):
        if length < 2:
            raise InvalidFilterFactoryParameter()

        if filter_type == "sma":
            return filters.sma.SMA(length)

        if filter_type == "wma":
            return filters.wma.WMA(length)

        if filter_type == "hma":
            return filters.hma.HMA(length)

        if filter_type == "derivative":
            return filters.derivative.Derivative(length)

        raise InvalidFilterFactoryParameter()
