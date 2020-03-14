#!/usr/bin/python3

import datetime


class IndicatorsStorage:
    def __init__(self, db):
        self.__collection = db.indicators

    def add(self, market: str, candle_size: str, value: float) -> bool:
        market_collection = self.__collection[market]
        candle_collection = market_collection[candle_size]
        candle_collection.insert_one({
            "date": datetime.datetime.utcnow(),
            "value": value
        })

    def get(self, market, candle_size, start_date, end_date):
        market_collection = self.__collection[market]
        candle_collection = market_collection[candle_size]
        if start_date and end_date:
            return candle_collection.find(
                {'time': {
                    '$gte': start_date,
                    '$lt': end_date
                }})
        if start_date:
            return candle_collection.find({'time': {
                '$gte': start_date,
            }})
        return candle_collection.find({'time': {'$lt': end_date}})
