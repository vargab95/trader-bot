#!/usr/bin/python3

import typing

import filters.sma
import filters.wma
import filters.hma
import filters.derivative
import filters.derivative_ratio
import filters.complex
import config.filter


class InvalidFilterFactoryParameter(Exception):
    pass


class FilterFactory:
    available_types = ["sma", "wma", "hma", "derivative", "derivative_ratio"]

    @staticmethod
    def create(configuration: config.filter.FilterConfig):
        # for Coefficient filter which can be used with WMA and EMA
        if configuration.length < 2:
            raise InvalidFilterFactoryParameter()

        if configuration.type == "sma":
            return filters.sma.SMA(configuration.length)

        if configuration.type == "wma":
            return filters.wma.WMA(configuration.length)

        if configuration.type == "hma":
            return filters.hma.HMA(configuration.length)

        if configuration.type == "derivative":
            return filters.derivative.Derivative(configuration.length)

        if configuration.type == "derivative_ratio":
            return filters.derivative_ratio.DerivativeRatio(configuration.length)

        raise InvalidFilterFactoryParameter(f"{configuration.type} is not a valid filter type")

    @staticmethod
    def create_complex(filter_specs: typing.List[config.filter.FilterConfig]):
        filt = filters.complex.Complex()

        for filter_spec in filter_specs:
            filt.add_filter(FilterFactory.create(filter_spec))

        return filt
