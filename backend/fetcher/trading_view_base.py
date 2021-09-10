#!/usr/bin/python3

import logging
import requests

import config.trader

from fetcher.interface import Fetcher


class TradingViewFetcherBase(Fetcher):
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

    def __init__(self, trader_config: config.trader.TraderConfig):
        self.request = None
        self.response = {}
        self.check_interval = trader_config.check_interval
        self.market_name = trader_config.market
        self.candle_size = trader_config.candle_size
        self.indicator_name = trader_config.indicator

    def safe_fetch(self):
        for _ in range(1000):
            try:
                self.fetch_technical_indicator()
                break
            except Exception as exception:  # pylint: disable=broad-except
                logging.critical("Unhandled exception: %s", str(exception))

    def fetch_technical_indicator(self):
        self.response = requests.post(self.url,
                                      json=self.request,
                                      timeout=5)
        self.response = self.response.json()

    def get_technical_indicator(self) -> float:
        pass  # pragma: no cover
