#!/usr/bin/python3

import storage.base
from signals.trading_signal import IndicatorSignalDescriptor, TradingSignal, TradingSignalPoint


class IndicatorsStorage(storage.base.StorageBase):
    def _generate_signal(self, fetched_signal) -> TradingSignal:
        return TradingSignal(data=[TradingSignalPoint(date=line["date"], value=line["value"])
                                   for line in fetched_signal], descriptor=None)

    def _get_collection(self, descriptor: IndicatorSignalDescriptor):
        indicators_collection = self._db.indicators
        market_collection = indicators_collection[descriptor.market]
        indicator_collection = market_collection[descriptor.indicator]
        candle_collection = indicator_collection[descriptor.candle_size]
        return candle_collection
