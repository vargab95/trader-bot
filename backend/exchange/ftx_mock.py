#!/usr/bin/python3

import requests

import exchange.interface
import exchange.guard
import exchange.mock_base


class FtxMock(exchange.mock_base.MockBase):
    base_coin = "USDT"
    api_url = "https://ftx.com/api/"
    markets_url = api_url + "markets/"

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market) -> float:
        if self._is_real_time:
            response = requests.get(self.markets_url + market.target + "/" +
                                    market.base)
            data = response.json()
            if data["success"]:
                return data["result"]["last"]
        return self.price_mock[market.key]
