#!/usr/bin/python3

import logging

import config.exchange
import config.testing
import exchange.interface
import exchange.guard
import exchange.mock_base


class FtxMock(exchange.mock_base.MockBase):
    base_coin = "USDT"

    def __init__(self, exchange_config: config.exchange.ExchangeConfig,
                 testing_config: config.testing.TestingConfig):
        super().__init__(exchange_config, testing_config)

    @exchange.guard.exchange_guard
    def get_price(self, market: exchange.interface.Market) -> float:
        if self._is_real_time:
            return float(
                self._client.get_ticker(symbol=market.key)["lastPrice"])
        return self.price_mock[market.key]
