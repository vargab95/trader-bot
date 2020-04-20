#!/usr/bin/python3

import time

import fetcher.base
import fetcher.single
import fetcher.multi

import applications.base


class GathererApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self._output_file_path: str
        self._market_list = list()

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()
        self._initialize_exchange()
        self._initialize_fetcher()
        self.__initialize_market_list()

    def __initialize_market_list(self):
        self._market_list = [
            self._configuration.exchange.watched_market,
            self._configuration.exchange.bearish_market,
            self._configuration.exchange.bullish_market
        ]

    def _run_application_logic(self):
        while True:
            for market in self._market_list:
                price = self._exchange.get_price(market)
                self._ticker_storage.add(market.target + market.base, price)

            self._fetcher.safe_fetch()
            indicators = self._fetcher.get_technical_indicator()

            if isinstance(self._fetcher,
                          fetcher.single.TradingViewFetcherSingle):
                if indicators:
                    self._indicator_storage.add(
                        self._configuration.market.name,
                        self._configuration.market.indicator_name,
                        self._configuration.market.candle_size, indicators)
            else:
                self.__process_indicator_response(indicators)

            time.sleep(self._configuration.market.check_interval)

    def __process_indicator_response(self, indicators):
        for market in self._configuration.market.name:
            for indicator in self._configuration.market.indicator_name:
                for candle in self._configuration.market.candle_size:
                    if indicators[market][indicator][candle]:
                        self._indicator_storage.add(
                            market, indicator, candle,
                            indicators[market][indicator][candle])
