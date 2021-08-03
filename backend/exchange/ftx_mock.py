#!/usr/bin/python3

import config.exchange

import exchange.interface
import exchange.guard
import exchange.mock_base
from exchange.ftx import FtxController

from signals.trading_signal import TradingSignal, TickerSignalDescriptor


class FtxMock(exchange.mock_base.MockBase):
    api_url = "https://ftx.com/api/"
    markets_url = api_url + "markets/"
    datetime_format = "%Y-%m-%dT%H:%M:%S+00:00"

    def __init__(self, exchange_config: config.exchange.ExchangeConfig):
        super().__init__(exchange_config)

        self.__real_exchange: FtxController = None
        if self._is_real_time:
            self.__real_exchange = FtxController(exchange_config)

    def set_real_time(self, real_time: bool) -> None:
        self._is_real_time = real_time

        if self._is_real_time and self.__real_exchange is None:
            self.__real_exchange = FtxController(self._configuration)

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "price", future: bool = False) -> float:
        if self._is_real_time:
            return self.__real_exchange.get_price(market, keyword, future)
        return self.price_mock[self.get_market_key(market)]

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        if self._is_real_time:
            return self.__real_exchange.get_price_history(descriptor, keyword)
        raise NotImplementedError("Mocked price history has not been implemented yet")

    def get_positions(self) -> exchange.interface.Balances:
        if self._is_real_time:
            return self.__real_exchange.get_positions()
        return self.price_mock

    def get_position(self, market: exchange.interface.Market) -> float:
        if self._is_real_time:
            return self.__real_exchange.get_position(market)
        return self.price_mock[self.get_market_key(market)]
