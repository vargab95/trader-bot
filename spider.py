#!/usr/bin/python3

import time
import requests

import config

class InvalidConfigurationException(Exception):
    pass

class CannotFetchDataException(Exception):
    pass

class TradingViewSpider:
    url = "https://scanner.tradingview.com/crypto/scan"

    candle_size_map = {
        "1m": "Recommend.All|1",
        "5m": "Recommend.All|5",
        "1h": "Recommend.All|60",
        "4h": "Recommend.All|240",
        "1d": "Recommend.All",
        "1W": "Recommend.All|1W",
        "1M": "Recommend.All|1M"
    }

    def __init__(self, market: config.MarketConfig):
        if market.candle_size not in list(self.candle_size_map.keys()):
            raise InvalidConfigurationException
        self.request = {
            "symbols": {
                "tickers": [
                    market.name
                ],
                "query": {
                    "types": []
                }
            },
            "columns": [
                self.candle_size_map[market.candle_size]
            ]
        }
        self.response = None
        self.check_interval = market.check_interval

    def safe_fetch(self):
        while True:
            try:
                self.fetch_technical_summary()
                break
            except CannotFetchDataException:
                continue

    def fetch_technical_summary(self):
        try:
            self.response = requests.post(self.url, json=self.request, timeout=5)
        except requests.exceptions.ConnectionError:
            print("Connection error")
            raise CannotFetchDataException
        except requests.exceptions.Timeout:
            print("Connection timeout")
            raise CannotFetchDataException
        if self.response.json()["totalCount"] != 1:
            raise InvalidConfigurationException

    def get_technical_summary(self):
        return self.response.json()["data"][0]["d"][0]

    def sleep_until_next_data(self):
        time.sleep(self.check_interval)
