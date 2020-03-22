#!/usr/bin/python3

import time
import logging
import requests

import config.market
import fetcher.common


class TradingViewFetcherBase:
    url = "https://scanner.tradingview.com/crypto/scan"

    # Recommend.MA
    # Recommend.Others
    candle_size_map = {
        "1m": "|1",
        "5m": "|5",
        "15m": "|15",
        "1h": "|60",
        "4h": "|240",
        "1D": "",
        "1W": "|1W",
        "1M": "|1M"
    }

    indicator_name_map = {
        "all": "Recommend.All",
        "SMA": "Recommend.MA",
        "oscillator": "Recommend.Other"
    }

    def __init__(self, market: config.market.MarketConfig, candle_size: float):
        self.request = None
        self.response = None
        self.check_interval = market.check_interval
        self.market_name = market.name
        self.candle_size = candle_size
        self.indicator_name = market.indicator_name

    def safe_fetch(self):
        while True:
            try:
                self.fetch_technical_indicator()
                break
            except fetcher.common.CannotFetchDataException:
                continue

    def fetch_technical_indicator(self):
        try:
            self.response = requests.post(self.url,
                                          json=self.request,
                                          timeout=5)
            self.response = self.response.json()
        except requests.exceptions.ConnectionError:
            logging.error("Connection error")
            raise fetcher.common.CannotFetchDataException
        except requests.exceptions.Timeout:
            logging.error("Connection timeout")
            raise fetcher.common.CannotFetchDataException

    def get_technical_indicator(self) -> float:
        pass

    def sleep_until_next_data(self):
        time.sleep(self.check_interval)
