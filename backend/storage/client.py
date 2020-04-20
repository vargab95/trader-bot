#!/usr/bin/python3

import pymongo
import pymongo.collection


class Client:
    def __init__(self, url, user, password):
        self._client = pymongo.MongoClient(url,
                                           username=user,
                                           password=password,
                                           authSource="trading_view_bot")

    @property
    def database(self):
        return self._client.trading_view_bot
