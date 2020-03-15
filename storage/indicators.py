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

    def get(self,
            market="",
            candle_size="",
            start_date=None,
            end_date=None,
            limit=-1):

        if not market or not candle_size:
            return None

        market_collection = self.__collection[market]
        candle_collection = market_collection[candle_size]

        result = None
        if start_date and end_date:
            result = candle_collection.find(
                {'date': {
                    '$gte': start_date,
                    '$lt': end_date
                }})
        elif start_date:
            result = candle_collection.find({'date': {
                '$gte': start_date,
            }})
        elif end_date:
            result = candle_collection.find({'time': {'$lt': end_date}})
        else:
            result = candle_collection.find()

        if limit > 0:
            result = result.sort([("timestamp", -1)]).limit(limit)

        return [{
            "date": line["date"],
            "value": line["value"]
        } for line in result]
