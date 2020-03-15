#!/usr/bin/python3

import datetime


class TickersStorage:
    def __init__(self, db):
        self.__collection = db.tickers

    def add(self, market: str, price: float) -> bool:
        market_collection = self.__collection[market]
        market_collection.insert_one({
            "date": datetime.datetime.utcnow(),
            "price": price
        })

    def get(self, market="", start_date=None, end_date=None, limit=-1):

        if not market:
            return None

        market_collection = self.__collection[market]

        result = None
        if start_date and end_date:
            result = market_collection.find(
                {'date': {
                    '$gte': start_date,
                    '$lt': end_date
                }})
        elif start_date:
            result = market_collection.find({'date': {
                '$gte': start_date,
            }})
        elif end_date:
            result = market_collection.find({'time': {'$lt': end_date}})
        else:
            result = market_collection.find()

        if limit > 0:
            result = result.sort([("timestamp", -1)]).limit(limit)

        return [{
            "date": line["date"],
            "price": line["price"]
        } for line in result]
