#!/usr/bin/python3

from flask_restful import Resource
from flask_jwt_extended import jwt_required

import filters.factory
from api.common import filter_results, get_default_parser


class Ticker(Resource):
    storage = None
    datetime_format = None

    def __init__(self):
        self.parser = get_default_parser()

    @jwt_required
    def post(self):
        request = self.parser.parse_args()
        step = request['step']
        filter_list = request['filter']

        result = self.storage.get(request['market'], request['start_date'],
                                  request['end_date'], request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(self.datetime_format)

        if filter_list:
            result = filter_results(result, filter_list, 'price')

        return result[::step]


class TickerOptions(Resource):
    @staticmethod
    @jwt_required
    def get():
        return {
            'market': [
                'BTCUSDT', 'BTCUSD', 'BEARUSDT', 'BEARUSD', 'BULLUSDT',
                'BULLUSD'
            ],
            'filter_types':
            filters.factory.FilterFactory.available_types
        }
