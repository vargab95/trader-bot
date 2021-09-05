#!/usr/bin/python3

import csv

from signals.trading_signal import TradingSignal, TradingSignalDescriptor
from config.fetcher import FetcherConfig

from fetcher.interface import Fetcher
from fetcher.common import CannotFetchDataException


class CSVFetcher(Fetcher):
    def __init__(self, config: FetcherConfig):
        self.__indicator: float = None
        self.__config: FetcherConfig = config

        self.__csvfile = open(self.__config.path, "r", newline="")
        dialect = csv.Sniffer().sniff(self.__csvfile.read(1024))
        self.__csvfile.seek(0)
        self.__reader = csv.reader(self.__csvfile, dialect)

    def __del__(self):
        self.__csvfile.close()

    def fetch_technical_indicator(self):
        try:
            self.__indicator = float(next(self.__reader)[1])
        except StopIteration as exc:
            raise CannotFetchDataException("No more data in the CSV file") from exc

    def get_technical_indicator(self) -> float:
        return self.__indicator

    def get_indicator_history(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        raise NotImplementedError
