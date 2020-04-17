#!/usr/bin/python3

import typing

import filters.sma
import filters.wma
import filters.hma
import filters.derivative
import filters.complex


class InvalidFilterFactoryParameter(Exception):
    pass


class FilterFactory:
    available_types = ["sma", "wma", "hma", "derivative"]

    @staticmethod
    def create(filter_type: str, length: int = 2):
        # TODO if EMA will be created create a new level in inheritance tree
        # for Coefficient filter which can be used with WMA and EMA
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

    @staticmethod
    def create_complex(filter_specs: typing.Dict[str, int]):
        filt = filters.complex.Complex()

        for filt_type, filt_length in filter_specs.items():
            filt.add_filter(FilterFactory.create(filt_type, filt_length))

        return filt
