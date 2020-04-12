#!/usr/bin/python3

from flask_restful import Resource

from api.common import get_sma, get_default_parser


class Ticker(Resource):
    storage = None
    datetime_format = None

    def __init__(self):
        self.parser = get_default_parser()

    def get(self):
        request = self.parser.parse_args()
        sma_len = request['sma']
        step = request['step']

        result = self.storage.get(request['market'], request['start_date'],
                                  request['end_date'], request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(self.datetime_format)

        if sma_len > 1:
            result = get_sma(result, sma_len, 'price')

        return result[::step]


class TickerOptions(Resource):
    @staticmethod
    def get():
        return {'market': ['BTCUSDT', 'BTCUSD']}
