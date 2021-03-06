#!/usr/bin/python3

import logging

from signals.trading_signal import TradingSignalDescriptor, TradingSignal
from exchange.interface import Market
import config.trader
import fetcher.common
import fetcher.trading_view_base


class TradingViewFetcherSingle(fetcher.trading_view_base.TradingViewFetcherBase):
    def __init__(self, trader_config: config.trader.TraderConfig):
        super().__init__(trader_config)

        if not isinstance(trader_config.market, Market) or \
                not isinstance(trader_config.indicator, str) or \
                not isinstance(self.candle_size, str):
            logging.critical("If one of the configurations is list, then "
                             "a multi fetcher should be used")
            raise fetcher.common.InvalidConfigurationException

        if self.candle_size not in list(self.candle_size_map.keys()):
            raise fetcher.common.InvalidConfigurationException

        if trader_config.indicator not in self.indicator_name_map.keys():
            raise fetcher.common.InvalidConfigurationException

        self.request = {
            "symbols": {
                "tickers": [trader_config.market.key()],
                "query": {
                    "types": []
                }
            },
            "columns": [
                self.indicator_name_map[self.indicator_name] +
                self.candle_size_map[self.candle_size]
            ]
        }

    def get_technical_indicator(self) -> float:
        try:
            return self.response["data"][0]["d"][0]
        except KeyError:
            logging.warning(
                "Key error occured while processing trading view response %s", str(self.response))
            return None

    def get_indicator_history(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        raise NotImplementedError  # pragma: no cover
