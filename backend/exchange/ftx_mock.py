#!/usr/bin/python3

import logging
import requests

import exchange.interface
import exchange.guard
import exchange.mock_base


class FtxMock(exchange.mock_base.MockBase):
    api_url = "https://ftx.com/api/"
    markets_url = api_url + "markets/"

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market) -> float:
        if self._is_real_time:
            response = requests.get(self.markets_url + market.target + "/" +
                                    market.base)
            data = response.json()

            logging.debug(
                "Price was requested for %s (FTX). Response is %s", market.key, str(data))

            if data["success"]:
                logging.debug("Last FTX price for %s is %f",
                              market.key, data["result"]["price"])
                return data["result"]["price"]
        return self.price_mock[market.key]
