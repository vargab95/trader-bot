#!/usr/bin/python3

from flask_restful import Resource

import filters.factory
from api.common import get_sma, get_default_parser


class Ticker(Resource):
    storage = None
    datetime_format = None

    def __init__(self):
        self.parser = get_default_parser()

    def get(self):
        request = self.parser.parse_args()
        ma_length = request['ma_length']
        ma_type = request['ma_type']
        step = request['step']

        result = self.storage.get(request['market'], request['start_date'],
                                  request['end_date'], request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(self.datetime_format)

        if ma_length > 1:
            result = get_sma(result, ma_type, ma_length, 'price')

        return result[::step]


class TickerOptions(Resource):
    @staticmethod
    def get():
        return {
            'market': [
                'BTCUSDT', 'BTCUSD', 'BEARUSDT', 'BEARUSD', 'BULLUSDT',
                'BULLUSD'
            ],
            'filter_types':
            filters.factory.FilterFactory.available_types
        }
