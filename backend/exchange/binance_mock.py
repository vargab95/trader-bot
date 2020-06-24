#!/usr/bin/python3

import binance

import config.exchange
import config.testing
import exchange.interface
import exchange.guard
import exchange.mock_base


class BinanceMock(exchange.mock_base.MockBase):
    def __init__(self, exchange_config: config.exchange.ExchangeConfig,
                 testing_config: config.testing.TestingConfig):
        super().__init__(testing_config)
        self._client = binance.client.Client(exchange_config.public_key,
                                             exchange_config.private_key)

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "lastPrice") -> float:
        if self._is_real_time:
            return float(
                self._client.get_ticker(symbol=market.key)[keyword])
        return self.price_mock[market.key]
