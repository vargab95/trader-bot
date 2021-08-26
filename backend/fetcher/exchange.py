#!/usr/bin/python3

from signals.trading_signal import TradingSignal, TradingSignalDescriptor
from config.fetcher import FetcherConfig
from exchange.interface import ExchangeInterface

from fetcher.interface import Fetcher


class ExchangeFetcher(Fetcher):
    def __init__(self, config: FetcherConfig, exchange: ExchangeInterface):
        self.__indicator: float = None
        self.__config: FetcherConfig = config
        self.__exchange: ExchangeInterface = exchange

    def fetch_technical_indicator(self):
        self.__indicator = self.__exchange.get_price(self.__config.market, future=self.__config.future)

    def get_technical_indicator(self) -> float:
        return self.__indicator

    def get_indicator_history(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        return self.__exchange.get_price_history(descriptor)
