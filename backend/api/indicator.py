#!/usr/bin/python3

from flask_restful import Resource
from flask_jwt_extended import jwt_required

import fetcher.base
import filters.factory
from api.common import filter_results, get_default_parser


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

    @jwt_required
    def post(self):
        request = self.parser.parse_args()
        filter_list = request['filter']
        step = request['step']

        result = self.storage.get(request['market'], request['indicator'],
                                  request['candle_size'],
                                  request['start_date'], request['end_date'],
                                  request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(self.datetime_format)

        if filter_list:
            result = filter_results(result, filter_list, 'value')

        return result[::step]


class IndicatorOptions(Resource):
    @staticmethod
    @jwt_required
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
