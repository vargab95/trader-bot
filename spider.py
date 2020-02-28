#!/usr/bin/python3

import time
import requests

class InvalidConfigurationException(Exception):
    pass

class TradingViewSpider:
    url = "https://scanner.tradingview.com/crypto/scan"

    period_map = {
        "1m": {
            "column": "Recommend.All|1",
            "period": 60
        },
        "5m": {
            "column": "Recommend.All|5",
            "period": 5 * 60
        },
        "1h": {
            "column": "Recommend.All|60",
            "period": 1 * 60 * 60
        },
        "4h": {
            "column": "Recommend.All|240",
            "period": 4 * 60 * 60
        },
        "1d": {
            "column": "Recommend.All",
            "period": 24 * 60 * 60
        },
        "1W": {
            "column": "Recommend.All|1W",
            "period": 7 * 24 * 60 * 60
        },
        # TODO 
        "1M": {
            "column": "Recommend.All|1M",
            "period": 31 * 24 * 60 * 60
        }
    }

    def __init__(self, market_name, period):
        if period not in list(self.period_map.keys()):
            raise InvalidConfigurationException
        self.request = {
            "symbols": {
                "tickers": [
                    market_name
                ],
                "query": {
                    "types": []
                }
            },
            "columns": [
                self.period_map[period]["column"]
            ]
        }
        self.response = None
        self.period_time = self.period_map[period]["period"]

    def fetch_technical_summary(self):
        self.response = requests.post(self.url, json=self.request)
        if self.response.json()["totalCount"] != 1:
            raise InvalidConfigurationException

    def get_technical_summary(self):
        if not self.response:
            self.fetch_technical_summary()
        return self.response.json()["data"][0]["d"][0]

    def sleep_until_next_data(self):
        time.sleep(self.period_time)
