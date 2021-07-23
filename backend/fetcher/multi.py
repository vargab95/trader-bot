#!/usr/bin/python3

import logging

import config.trader
import fetcher.common
import fetcher.trading_view_base


class TradingViewFetcherMulti(fetcher.trading_view_base.TradingViewFetcherBase):
    def __init__(self, trader_config: config.trader.TraderConfig):
        super().__init__(trader_config)

        self.request = {
            "symbols": {
                "tickers": [],
                "query": {
                    "types": []
                }
            },
            "columns": []
        }

        if isinstance(trader_config.market, list):
            self.request["symbols"]["tickers"] = self.market_name
        else:
            self.request["symbols"]["tickers"] = [self.market_name]

        try:
            if isinstance(self.candle_size, list) and \
                    isinstance(self.indicator_name, list):
                for candle in self.candle_size:
                    for indicator in self.indicator_name:
                        self.request["columns"].append(
                            self.indicator_name_map[indicator] +
                            self.candle_size_map[candle])
            elif not isinstance(self.candle_size, list) and \
                    isinstance(self.indicator_name, list):
                self.request["columns"] = [
                    self.indicator_name_map[i] +
                    self.candle_size_map[self.candle_size]
                    for i in self.indicator_name
                ]
            elif isinstance(self.candle_size, list) and \
                    not isinstance(self.indicator_name, list):
                self.request["columns"] = [
                    self.indicator_name_map[self.indicator_name] +
                    self.candle_size_map[c] for c in self.candle_size
                ]
            else:
                self.request["columns"] = [
                    self.indicator_name_map[self.indicator_name] +
                    self.candle_size_map[self.candle_size]
                ]
        except KeyError:
            raise fetcher.common.InvalidConfigurationException()

    def get_technical_indicator(self) -> float:
        try:
            return self.__process_response()
        except KeyError:
            logging.warning(
                "Key error occured while processing trading view response %s", str(self.response))

        return []

    def __process_response(self):
        data = {}
        for market_data in self.response["data"]:
            data[market_data["s"]] = {}
            i = 0
            for value in market_data["d"]:
                elements = self.request["columns"][i].split('|')
                for key, name in self.indicator_name_map.items():
                    if name == elements[0]:
                        indicator = key

                if len(elements) == 1:
                    candle_size = "1D"
                else:
                    for key, candle in self.candle_size_map.items():
                        if candle == ('|' + elements[1]):
                            candle_size = key

                if indicator not in data[market_data["s"]].keys():
                    data[market_data["s"]][indicator] = {}

                data[market_data["s"]][indicator][candle_size] = value
                i += 1
        return data
