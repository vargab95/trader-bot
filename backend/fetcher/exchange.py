#!/usr/bin/python3

from config.fetcher import FetcherConfig
from exchange.interface import ExchangeInterface

from fetcher.interface import Fetcher


class ExchangeFetcher(Fetcher):
    def __init__(self, config: FetcherConfig, exchange: ExchangeInterface):
        self.__indicator: float = None
        self.__config: FetcherConfig = config
        self.__exchange: ExchangeInterface = exchange

    def fetch_technical_indicator(self):
        self.__indicator = self.__exchange.get_price(self.__config.market)

    def get_technical_indicator(self) -> float:
        return self.__indicator
