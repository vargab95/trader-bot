#!/usr/bin/python3

import csv

from signals.trading_signal import TradingSignal, TradingSignalDescriptor
from config.fetcher import FetcherConfig

from fetcher.interface import Fetcher


class CSVFetcher(Fetcher):
    def __init__(self, config: FetcherConfig):
        self.__indicator: float = None
        self.__config: FetcherConfig = config

        with open(self.__config.path, "r", newline="") as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            self.__reader = csv.reader(csvfile, dialect)

    def fetch_technical_indicator(self):
        self.__indicator = next(self.__reader)[1]

    def get_technical_indicator(self) -> float:
        return self.__indicator

    def get_indicator_history(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        raise NotImplementedError
