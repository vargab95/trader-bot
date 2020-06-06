#!/usr/bin/python3

import storage.base
from signals.trading_signal import TickerSignalDescriptor, TradingSignal, TradingSignalPoint


class TickersStorage(storage.base.StorageBase):
    def __init__(self, db):
        super().__init__(db)
        self._value_key = "price"

    def _generate_signal(self, fetched_signal) -> TradingSignal:
        return TradingSignal(data=[TradingSignalPoint(date=line["date"], value=line["price"])
                                   for line in fetched_signal], descriptor=None)

    def _get_collection(self, descriptor: TickerSignalDescriptor):
        tickers_collection = self._db.tickers
        return tickers_collection[descriptor.market]
