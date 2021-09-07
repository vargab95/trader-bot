#!/usr/bin/python3

import typing

import filters.sma
import filters.wma
import filters.hma
import filters.nth
import filters.derivative
import filters.derivative_ratio
import filters.complex
import filters.rsi
import filters.macd
import config.filter


class InvalidFilterFactoryParameter(Exception):
    pass


class FilterFactory:
    @staticmethod
    def create(configuration: config.filter.FilterConfig):
        # for Coefficient filter which can be used with WMA and EMA
        if configuration.length < 2:
            raise InvalidFilterFactoryParameter()

        constructor_map = {
            "sma": filters.sma.SMA,
            "wma": filters.wma.WMA,
            "hma": filters.hma.HMA,
            "nth": filters.nth.NthFilter,
            "derivative": filters.derivative.Derivative,
            "derivative_ratio": filters.derivative_ratio.DerivativeRatio,
            "rsi": filters.rsi.RSI,
            "macd": filters.macd.MACD
        }

        try:
            return constructor_map[configuration.type](configuration)
        except KeyError as exc:
            raise InvalidFilterFactoryParameter(f"{configuration.type} is not a valid filter type") from exc

    @staticmethod
    def create_complex(filter_specs: typing.List[config.filter.FilterConfig]):
        filt = filters.complex.Complex()

        for filter_spec in filter_specs:
            filt.add_filter(FilterFactory.create(filter_spec))

        return filt
