#!/usr/bin/python3

from config.fetcher import FetcherConfig
from fetcher.single import TradingViewFetcherSingle
from fetcher.multi import TradingViewFetcherMulti
from fetcher.exchange import ExchangeFetcher
from fetcher.csv import CSVFetcher
from exchange.interface import ExchangeInterface


class InvalidFetcherFactoryParameter(Exception):
    pass


class FetcherFactory:
    @staticmethod
    def create(config: FetcherConfig, exchange: ExchangeInterface = None):
        if config.type == "trading_view":
            if isinstance(config.candle_size, str):
                return TradingViewFetcherSingle(config)

            if isinstance(config.candle_size, list):
                return TradingViewFetcherMulti(config)

        if config.type == "exchange":
            return ExchangeFetcher(config, exchange)

        if config.type == "csv_file":
            return CSVFetcher(config)

        raise InvalidFetcherFactoryParameter()
