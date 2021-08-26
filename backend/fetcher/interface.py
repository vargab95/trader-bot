#!/usr/bin/python3

import abc

from signals.trading_signal import TradingSignalDescriptor, TradingSignal


class Fetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_technical_indicator(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_technical_indicator(self) -> float:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_indicator_history(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        pass  # pragma: no cover
