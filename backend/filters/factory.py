#!/usr/bin/python3

import typing

import filters.sma
import filters.wma
import filters.hma
import filters.derivative
import filters.complex
import config.filter


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
    def create_complex(filter_specs: typing.List[config.filter.FilterConfig]):
        filt = filters.complex.Complex()

        for filter_spec in filter_specs:
            filt.add_filter(
                FilterFactory.create(filter_spec.type,
                                     filter_spec.length))

        return filt
