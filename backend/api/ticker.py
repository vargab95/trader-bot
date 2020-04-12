#!/usr/bin/python3

from flask_restful import reqparse, Resource

from api.common import convert_date_time, get_sma


class Ticker(Resource):
    storage = None
    datetime_format = None

    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('market', type=str, required=True)
        self.parser.add_argument('start_date', type=convert_date_time)
        self.parser.add_argument('end_date', type=convert_date_time)
        self.parser.add_argument('limit', type=int, default=-1)
        self.parser.add_argument('sma', type=int, default=-1)
        self.parser.add_argument('step', type=int, default=1)

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
    def get(self):
        return {'market': ['BTCUSDT', 'BTCUSD']}
