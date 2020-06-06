#!/usr/bin/python3

import abc
from datetime import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

import filters.factory
from signals.trading_signal import TradingSignalDescriptor


class Signal(Resource):
    storage = None
    datetime_format = None
    DATE_TIME_FORMAT = ""

    def __init__(self):
        self._parser = reqparse.RequestParser()

        self._parser.add_argument('market', type=str, required=True)
        self._parser.add_argument('dateSpan', type=dict)
        self._parser.add_argument('limit', type=int, default=-1)
        self._parser.add_argument('step', type=int, default=1)
        self._parser.add_argument('filter', type=dict, action="append")

    @jwt_required
    def post(self):
        request = self._parser.parse_args()
        filter_list = request['filter']

        descriptor = self._compose_descriptor(request)

        result = self.storage.get(descriptor)

        for row in result.data:
            row.date = row.date.strftime(self.datetime_format)

        if filter_list:
            result = self._filter_results(result, filter_list)

        return result[::result.descriptor.step]

    @staticmethod
    def _convert_date_time(date_string):
        return datetime.strptime(date_string, Signal.DATE_TIME_FORMAT)

    @staticmethod
    def _filter_results(values, filter_list):
        complex_filter = filters.factory.FilterFactory.create_complex(
            filter_list)

        result = []
        for row in values.data:
            complex_filter.put(row.value)
            filtered = complex_filter.get()
            if filtered:
                row.value = filtered
                result.append(row)

        values.data = result

        return values

    @abc.abstractmethod
    def _compose_descriptor(self, request) -> TradingSignalDescriptor:
        pass
