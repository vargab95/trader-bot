#!/usr/bin/python3

from flask_restful import Resource
from flask_jwt_extended import jwt_required

import filters.factory
from signals.trading_signal import TickerSignalDescriptor
from api.signals import Signal


class Ticker(Signal):
    def _compose_descriptor(self, request) -> TickerSignalDescriptor:
        return TickerSignalDescriptor(
            market=request['market'],
            start_date=self._convert_date_time(request['dateSpan']['start']),
            end_date=self._convert_date_time(request['dateSpan']['end']),
            limit=request['limit'],
            step=request['step']
        )


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
