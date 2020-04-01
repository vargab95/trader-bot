#!/usr/bin/python3

import requests

import config.exchange
import config.testing
import exchange.interface
import exchange.guard
import exchange.mock_base


class FtxMock(exchange.mock_base.MockBase):
    base_coin = "USDT"
    api_url = "https://ftx.com/api/"
    markets_url = api_url + "markets/"

    def __init__(self, exchange_config: config.exchange.ExchangeConfig,
                 testing_config: config.testing.TestingConfig):
        super().__init__(exchange_config, testing_config)

    @exchange.guard.exchange_guard
    def get_price(self, market: exchange.interface.Market) -> float:
        if self._is_real_time:
            response = requests.get(self.markets_url + market.target + "/" +
                                    market.base)
            data = response.json()
            if data["success"]:
                return data["result"]["last"]
        return self.price_mock[market.key]
