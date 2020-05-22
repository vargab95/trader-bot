#!/usr/bin/python3

import logging

import config.trader
import fetcher.common
import fetcher.base


# TODO Not covered by tests
class TradingViewFetcherSingle(fetcher.base.TradingViewFetcherBase):
    def __init__(self, market: config.trader.TraderConfig, candle_size: float):
        super().__init__(market, candle_size)

        if candle_size not in list(self.candle_size_map.keys()):
            raise fetcher.common.InvalidConfigurationException

        if market.indicator_name not in self.indicator_name_map.keys():
            raise fetcher.common.InvalidConfigurationException

        if not isinstance(market.name, str) or \
                not isinstance(market.indicator_name, str) or \
                not isinstance(market.candle_size, str):
            logging.critical("If one of the configurations is list, then "
                             "a multi fetcher should be used")
            raise fetcher.common.InvalidConfigurationException

        self.request = {
            "symbols": {
                "tickers": [market.name],
                "query": {
                    "types": []
                }
            },
            "columns": [
                self.indicator_name_map[self.indicator_name] +
                self.candle_size_map[candle_size]
            ]
        }

    def get_technical_indicator(self) -> float:
        return self.response["data"][0]["d"][0]
