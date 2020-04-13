#!/usr/bin/python3

import filters.sma
import filters.wma
import filters.hma


class InvalidFilterType(Exception):
    pass


class FilterFactory:
    available_types = ["sma", "wma", "hma"]

    @staticmethod
    def create(ma_type: str, length: int):
        if ma_type == "sma":
            return filters.sma.SMA(length)

        if ma_type == "wma":
            return filters.wma.WMA(length)

        if ma_type == "hma":
            return filters.hma.HMA(length)

        raise InvalidFilterType()
