#!/usr/bin/python3

import time

import fetcher.single
import fetcher.multi

import applications.base

from signals.trading_signal import IndicatorSignalDescriptor, TickerSignalDescriptor, TradingSignalPoint


class GathererApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self._output_file_path: str
        self._market_list = list()

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()
        self._builder.create_exchanges(self._configuration.components.exchanges)
        self._builder.create_fetchers(self._configuration.components.fetchers)
        self.__initialize_market_list()

    def __initialize_market_list(self):
        self._market_list = [
            self._configuration.exchange.watched_market,
            self._configuration.exchange.bearish_market,
            self._configuration.exchange.bullish_market
        ]

    def _run_application_logic(self):
        raise NotImplementedError()
        # exchange = self._builder.exchanges[self._configuration.gatherer.exchange_id]

        # TODO Implement gatherer with the new architecture
        # while True:
        #     for market in self._market_list:
        #         price = exchange.get_price(market)
        #         self._ticker_storage.add(TickerSignalDescriptor(market=market.target + market.base),
        #                                  TradingSignalPoint(value=price))

        #     self._fetcher.safe_fetch()
        #     indicators = self._fetcher.get_technical_indicator()

        #     if isinstance(self._fetcher, fetcher.single.TradingViewFetcherSingle):
        #         if indicators:
        #             self._indicator_storage.add(
        #                 IndicatorSignalDescriptor(market=self._configuration.trader.market,
        #                                           indicator=self._configuration.trader.indicator,
        #                                           candle_size=self._configuration.trader.candle_size),
        #                 TradingSignalPoint(value=indicators))
        #     else:
        #         self.__process_indicator_response(indicators)

        #     time.sleep(self._configuration.trader.check_interval)

    def __process_indicator_response(self, indicators):
        for market in self._configuration.trader.name:
            for indicator in self._configuration.trader.indicator_name:
                for candle in self._configuration.trader.candle_size:
                    if indicators[market][indicator][candle]:
                        self._indicator_storage.add(
                            IndicatorSignalDescriptor(market=market, indicator=indicator, candle_size=candle),
                            TradingSignalPoint(value=indicators[market][indicator][candle])
                        )
