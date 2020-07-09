#!/usr/bin/python3

import logging
import datetime
import traceback
import requests

import exchange.interface
import exchange.guard
import exchange.mock_base

from signals.trading_signal import TradingSignal, TickerSignalDescriptor, TradingSignalPoint


class FtxMock(exchange.mock_base.MockBase):
    api_url = "https://ftx.com/api/"
    markets_url = api_url + "markets/"
    datetime_format = "%Y-%m-%dT%H:%M:%S+00:00"

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "price") -> float:
        if self._is_real_time:
            response = requests.get(self.markets_url + market.target + "/" +
                                    market.base)
            data = response.json()

            logging.debug(
                "Price was requested for %s (FTX). Response is %s", market.key, str(data))

            if data["success"]:
                logging.debug("Last FTX price for %s is %f",
                              market.key, data["result"][keyword])
                return data["result"][keyword]
        return self.price_mock[market.key]

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        if self._is_real_time:
            valid_resolutions = [15, 60, 300, 900, 3600, 14400, 86400]

            if descriptor.resolution.total_seconds() not in valid_resolutions:
                raise ValueError(
                    "Resolution time gap " + str(descriptor.resolution.total_seconds()) +
                    " should be in " + str(valid_resolutions))

            request_url = self.markets_url + descriptor.market.key + "/candles"
            request_url += "?resolution=" + \
                str(int(descriptor.resolution.total_seconds()))

            if descriptor.limit > 0:
                request_url += "&limit=" + str(descriptor.limit)

            if descriptor.start_date is not None:
                request_url += "&start_time=" + \
                    str(int((descriptor.start_date
                             - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))

            if descriptor.end_date is not None:
                request_url += "&end_time=" + \
                    str(int((descriptor.end
                             - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))

            logging.debug("FTX price history request: %s", request_url)
            response = requests.get(request_url)
            data = response.json()

            if not data["success"]:
                logging.error("Could not get historical data of %s",
                              str(descriptor.market))
                logging.error("%s\n\n%s", str(data["error"]),
                              ''.join(traceback.format_stack()))
                raise exchange.interface.ExchangeError(data["error"])

            logging.debug("FTX price history request result: %s", str(data))

            history = []
            for item in data["result"]:
                point = TradingSignalPoint()
                point.value = float(item[keyword])
                point.date = datetime.datetime.strptime(
                    item["startTime"], self.datetime_format)
                history.append(point)

            return TradingSignal(history, descriptor)
        raise NotImplementedError(
            "Mocked price history has not been implemented yet")
