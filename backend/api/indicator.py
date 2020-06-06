#!/usr/bin/python3

from flask_restful import Resource
from flask_jwt_extended import jwt_required

import fetcher.base
import filters.factory
from signals.trading_signal import IndicatorSignalDescriptor
from api.signals import Signal


class Indicator(Signal):
    def __init__(self):
        super().__init__()

        self._parser.add_argument(
            'indicator',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.indicator_name_map.keys()),
            required=True)

        self._parser.add_argument(
            'candleSize',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            required=True)

    def _compose_descriptor(self, request) -> IndicatorSignalDescriptor:
        return IndicatorSignalDescriptor(
            market=request['market'],
            indicator=request['indicator'],
            candle_size=request['candleSize'],
            start_date=self._convert_date_time(request['dateSpan']['start']),
            end_date=self._convert_date_time(request['dateSpan']['end']),
            limit=request['limit'],
            step=request['step']
        )


class IndicatorOptions(Resource):
    @staticmethod
    @jwt_required
    def get():
        return {
            'market': ['GEMINI:BTCUSD', 'FTX:BEARUSD', 'FTX:BEARUSDT', 'FTX:BULLUSD', 'FTX:BULLUSDT'],
            'candle_size':
            list(fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            'indicator':
            list(
                fetcher.base.TradingViewFetcherBase.indicator_name_map.keys()),
            'filter_types':
            filters.factory.FilterFactory.available_types
        }
