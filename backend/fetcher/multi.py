#!/usr/bin/python3

import config.market
import fetcher.common
import fetcher.base


# TODO Not covered by tests
class TradingViewFetcherMulti(fetcher.base.TradingViewFetcherBase):
    def __init__(self, market: config.market.MarketConfig, candle_size: float):
        super().__init__(market, candle_size)

        self.request = {
            "symbols": {
                "tickers": [],
                "query": {
                    "types": []
                }
            },
            "columns": []
        }

        if isinstance(market.name, list):
            self.request["symbols"]["tickers"] = self.market_name
        else:
            self.request["symbols"]["tickers"] = [self.market_name]

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

    def get_technical_indicator(self) -> float:
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
