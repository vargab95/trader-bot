#!/usr/bin/python3

import abc

from signals.trading_signal import TradingSignalDescriptor, TradingSignal, TradingSignalPoint


class StorageInterface:
    @abc.abstractmethod
    def add(self, descriptor: TradingSignalDescriptor, point: TradingSignalPoint) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get(self, descriptor: TradingSignalDescriptor) -> TradingSignal:  # pragma: no cover
        pass
