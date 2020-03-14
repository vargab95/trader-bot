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

    def get(self, market, start_date, end_date):
        market_collection = self.__collection[market]
        if start_date and end_date:
            return market_collection.find(
                {'time': {
                    '$gte': start_date,
                    '$lt': end_date
                }})
        if start_date:
            return market_collection.find({'time': {
                '$gte': start_date,
            }})
        return market_collection.find({'time': {'$lt': end_date}})
