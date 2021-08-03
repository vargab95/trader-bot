#!/usr/bin/python3

import time
import datetime
import hmac
import logging
import json
import traceback
import requests

import config.exchange
import exchange.base
import exchange.interface
import exchange.guard

from signals.trading_signal import TradingSignal, TickerSignalDescriptor, TradingSignalPoint


class FtxController(exchange.base.ExchangeBase):
    api_url = "https://ftx.com/api/"
    markets_url = "markets/"
    balances_url = "wallet/balances"
    orders_url = "orders"
    futures_url = "futures/"
    positions_url = "positions"
    account_url = "account"
    datetime_format = "%Y-%m-%dT%H:%M:%S+00:00"

    def __init__(self, configuration: config.exchange.ExchangeConfig):
        super().__init__(configuration)
        response = requests.get(self.api_url + "markets").json()
        if not response["success"]:
            logging.error("Could not get markets during init")
            raise exchange.interface.ExchangeError(response["error"])

        logging.debug("Minimal values:")
        for market in response["result"]:
            self._min_amount[market["name"]] = market["minProvideSize"]
            self._min_notional[market["name"]] = market["priceIncrement"]
            logging.debug("\t%s amount: %.12f price: %.12f", market["name"],
                          market["minProvideSize"], market["priceIncrement"])

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        if amount <= 0.0:
            return False

        corrected_amount = self._check_and_log_corrected_amount(
            market, amount, "buy")

        if corrected_amount <= 0.0:
            return False

        if not self.__send_authenticated_request('POST',
                                                 self.orders_url,
                                                 data={
                                                     "market": self.get_market_key(market),
                                                     "side": "buy",
                                                     "type": "market",
                                                     "size": corrected_amount,
                                                     "price": None
                                                 }):
            return False

        logging.info("%.10f %s was successfully bought", corrected_amount, self.get_market_key(market))

        return True

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        if amount <= 0.0:
            return False

        corrected_amount = self._check_and_log_corrected_amount(market, amount, "sell")

        if corrected_amount <= 0.0:
            return False

        if not self.__send_authenticated_request('POST',
                                                 self.orders_url,
                                                 data={
                                                     "market": self.get_market_key(market),
                                                     "side": "sell",
                                                     "type": "market",
                                                     "size": corrected_amount,
                                                     "price": None
                                                 }):
            return False

        logging.info("%.10f %s was successfully sold", corrected_amount, self.get_market_key(market))

        return True

    def get_balances(self) -> exchange.interface.Balances:
        balances = self.__send_authenticated_request('GET', self.balances_url)

        result = exchange.interface.Balances()
        for balance in balances:
            free = float(balance["free"])
            if free > 1e-7:
                result[balance["coin"]] = free

        return result

    def get_balance(self, market: str) -> float:
        balances = self.get_balances()

        for key, value in balances.items():
            if key == market:
                return value

        return 0.0

    def get_positions(self) -> exchange.interface.Balances:
        balances = self.__send_authenticated_request('GET', self.positions_url)

        result = exchange.interface.Balances()
        for balance in balances:
            net_size = float(balance["netSize"])
            if abs(net_size) > 1e-7:
                result[balance["future"]] = net_size

        return result

    def get_position(self, market: exchange.interface.Market) -> float:
        balances = self.get_positions()

        for key, value in balances.items():
            if key == self.get_market_key(market):
                return value

        return 0.0

    def get_leverage_balance(self) -> float:
        account_info = self.__send_authenticated_request("GET", self.account_url)

        return account_info["totalAccountValue"] * account_info["leverage"] - account_info["totalPositionSize"]

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "price", future: bool = False) -> float:
        if future:
            used_url = self.futures_url
            # There is no price key on futures...
            if keyword == "price":
                keyword = "ask"
        else:
            used_url = self.markets_url
        response = requests.get(self.api_url + used_url + self.get_market_key(market))
        data = response.json()

        logging.debug("Price was requested for %s (FTX). Response is %s", self.get_market_key(market), str(data))

        if data["success"]:
            logging.debug("Last FTX price for %s is %f", self.get_market_key(market), data["result"][keyword])
            return data["result"][keyword]

        logging.error("Could not get price of %s", str(market))
        logging.error("%s\n\n%s", str(data["error"]), ''.join(traceback.format_stack()))
        raise exchange.interface.ExchangeError(data["error"])

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        valid_resolutions = [15, 60, 300, 900, 3600, 14400, 86400]

        if descriptor.resolution.total_seconds() not in valid_resolutions:
            raise ValueError("Resolution time gap should be in " + str(valid_resolutions))

        request_url = self.api_url + self.markets_url + self.get_market_key(descriptor.market) + "/candles"
        request_url += "?resolution=" + str(int(descriptor.resolution.total_seconds()))

        if descriptor.limit > 0:
            request_url += "&limit=" + str(descriptor.limit)

            if descriptor.start_date is not None:
                request_url += "&start_time=" + \
                    str(int((descriptor.start_date - datetime.datetime(1970, 1, 1)).total_seconds()))

            if descriptor.end_date is not None:
                request_url += "&end_time=" + \
                    str(int((descriptor.end_date - datetime.datetime(1970, 1, 1)).total_seconds()))

        logging.debug("FTX price history request: %s", request_url)
        response = requests.get(request_url)
        data = response.json()

        if not data["success"]:
            logging.error("Could not get historical data of %s", str(descriptor.market))
            logging.error("%s\n\n%s", str(data["error"]), ''.join(traceback.format_stack()))
            raise exchange.interface.ExchangeError(data["error"])

        logging.debug("FTX price history request result: %s", str(data))

        history = []
        for item in data["result"]:
            point = TradingSignalPoint()
            point.value = float(item[keyword])
            point.date = datetime.datetime.strptime(item["startTime"], self.datetime_format)
            history.append(point)

        return TradingSignal(history, descriptor)

    @exchange.guard.exchange_guard()
    def __send_authenticated_request(self, method, endpoint, data=None):
        timestamp = int(time.time() * 1000)

        session = requests.Session()
        request = requests.Request(method, self.api_url + endpoint)
        request.json = data

        prepared = request.prepare()
        signature_payload = f'{timestamp}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._private_key.encode(), signature_payload, 'sha256').hexdigest()

        prepared.headers['FTX-KEY'] = self._public_key
        prepared.headers['FTX-SIGN'] = signature
        prepared.headers['FTX-TS'] = str(timestamp)
        prepared.headers['Content-type'] = 'application/json'

        response = session.send(prepared)
        response_body = response.json()

        logging.debug("[%s] %s (%s) -> %d\n%s", method, endpoint, str(data),
                      response.status_code, json.dumps(response_body, indent=4))

        if not response_body["success"]:
            raise exchange.interface.ExchangeError(response_body["error"])

        return response_body["result"]
