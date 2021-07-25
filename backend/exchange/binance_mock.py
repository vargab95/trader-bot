#!/usr/bin/python3

import logging
import datetime
import binance
import binance.client

import config.exchange
import config.testing
import exchange.interface
import exchange.guard
import exchange.mock_base

from signals.trading_signal import TradingSignal, TickerSignalDescriptor, TradingSignalPoint


class BinanceMock(exchange.mock_base.MockBase):
    def __init__(self, exchange_config: config.exchange.ExchangeConfig):
        super().__init__(exchange_config)
        self._client = binance.client.Client(exchange_config.public_key,
                                             exchange_config.private_key)

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "lastPrice", future: bool = False) -> float:
        if self._is_real_time:
            return float(self._client.get_ticker(symbol=market.key)[keyword])
        return self.price_mock[market.key]

    # FIXME DUPLICATE!!!
    __resolution_map = {
        60:             binance.client.Client.KLINE_INTERVAL_1MINUTE,
        60 * 3:         binance.client.Client.KLINE_INTERVAL_3MINUTE,
        60 * 5:         binance.client.Client.KLINE_INTERVAL_5MINUTE,
        60 * 15:        binance.client.Client.KLINE_INTERVAL_15MINUTE,
        60 * 30:        binance.client.Client.KLINE_INTERVAL_30MINUTE,
        3600:           binance.client.Client.KLINE_INTERVAL_1HOUR,
        3600 * 2:       binance.client.Client.KLINE_INTERVAL_2HOUR,
        3600 * 4:       binance.client.Client.KLINE_INTERVAL_4HOUR,
        3600 * 6:       binance.client.Client.KLINE_INTERVAL_6HOUR,
        3600 * 8:       binance.client.Client.KLINE_INTERVAL_8HOUR,
        3600 * 12:      binance.client.Client.KLINE_INTERVAL_12HOUR,
        3600 * 24:      binance.client.Client.KLINE_INTERVAL_1DAY,
        3600 * 24 * 3:  binance.client.Client.KLINE_INTERVAL_3DAY,
        3600 * 24 * 7:  binance.client.Client.KLINE_INTERVAL_1WEEK,
        3600 * 24 * 30: binance.client.Client.KLINE_INTERVAL_1MONTH
    }

    __result_map = {
        "time": 0,
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4,
        "volume": 5
    }

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        if self._is_real_time:
            if descriptor.resolution.total_seconds() not in list(self.__resolution_map.keys()):
                raise ValueError(
                    "Resolution time gap should be in " + str(list(self.__resolution_map.keys())))

            resolution = self.__resolution_map[
                descriptor.resolution.total_seconds()]

            result = self._client.get_historical_klines(
                symbol=descriptor.market.key,
                interval=str(resolution),
                start_str=int((descriptor.start_date
                               - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) if descriptor.start_date else 0,
                end_str=int((descriptor.end_date -
                             datetime.datetime(1970, 1, 1)).total_seconds())
                * 1000 if descriptor.end_date else None,
                limit=descriptor.limit if descriptor.limit > 0 else 500
            )

            logging.debug(
                "Binance price history request result: %s", str(result))

            history = []
            for item in result:
                point = TradingSignalPoint()
                point.value = float(item[self.__result_map[keyword]])
                point.date = datetime.datetime.fromtimestamp(item[0] / 1000)
                history.append(point)

            return TradingSignal(history, descriptor)
        raise NotImplementedError(
            "Mocked price history has not been implemented yet")

    def get_positions(self) -> exchange.interface.Balances:
        raise NotImplementedError

    def get_position(self, market: str) -> float:
        raise NotImplementedError
