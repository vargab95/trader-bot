#!/usr/bin/python3

from flask_restful import Resource

import fetcher.base
import filters.factory
from api.common import get_sma, get_default_parser


class Indicator(Resource):
    storage = None
    datetime_format = None

    def __init__(self):
        self.parser = get_default_parser()

        self.parser.add_argument(
            'indicator',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.indicator_name_map.keys()),
            required=True)

        self.parser.add_argument(
            'candle_size',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            required=True)

    def get(self):
        request = self.parser.parse_args()
        sma_len = request['sma']
        step = request['step']

        result = self.storage.get(request['market'], request['indicator'],
                                  request['candle_size'],
                                  request['start_date'], request['end_date'],
                                  request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(self.datetime_format)

        if sma_len > 1:
            result = get_sma(result, sma_len, 'value')

        return result[::step]


class IndicatorOptions(Resource):
    @staticmethod
    def get():
        return {
            'market': ['GEMINI:BTCUSD'],
            'candle_size':
            list(fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            'indicator':
            list(
                fetcher.base.TradingViewFetcherBase.indicator_name_map.keys()),
            'filter_types':
            filters.factory.FilterFactory.available_types
        }
