#!/usr/bin/python3

import time
import hmac
import logging
import traceback
import requests

import config.exchange
import exchange.base
import exchange.interface
import exchange.guard


class FtxController(exchange.base.ExchangeBase):
    api_url = "https://ftx.com/api/"
    markets_url = "markets/"
    balances_url = "wallet/balances"
    orders_url = "orders"

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
        corrected_amount = self._floor(amount, self._min_amount[market.key])
        logging.info("Trying to buy %.10f %s", corrected_amount, market.key)
        logging.debug("%.10f was corrected to %.10f", amount, corrected_amount)

        if not self._is_enough_amount(market, corrected_amount):
            logging.warning("Buy failed due to insufficient resources.")
            return False

        logging.debug("Corrected amount string: %f", corrected_amount)
        self.__send_authenticated_request('POST',
                                          self.orders_url,
                                          data={
                                              "market": market.key,
                                              "side": "buy",
                                              "type": "market",
                                              "size": corrected_amount,
                                              "price": None
                                          })
        logging.info("%.10f %s was successfully bought", corrected_amount,
                     market.key)
        return True

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self._floor(amount, self._min_amount[market.key])
        logging.info("Trying to sell %.10f %s", corrected_amount, market.key)
        logging.debug("%.10f was corrected to %.10f", amount, corrected_amount)

        if not self._is_enough_amount(market, corrected_amount):
            logging.warning("Sell failed due to insufficient resources.")
            return False

        correted_amount_str = "{:.12f}".format(corrected_amount).rstrip('0')
        logging.debug("Corrected amount string: %s", correted_amount_str)
        self.__send_authenticated_request('POST',
                                          self.orders_url,
                                          data={
                                              "market": market.key,
                                              "side": "sell",
                                              "type": "market",
                                              "size": corrected_amount,
                                              "price": None
                                          })
        logging.info("%.10f %s was successfully sold", corrected_amount,
                     market.key)
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

    @exchange.guard.exchange_guard
    def get_price(self, market: exchange.interface.Market) -> float:
        response = requests.get(self.api_url + self.markets_url + market.key)
        data = response.json()

        if data["success"]:
            return data["result"]["last"]

        logging.error("Could not get price of %s", str(market))
        logging.error("%s\n\n%s", str(data["error"]),
                      ''.join(traceback.format_stack()))
        raise exchange.interface.ExchangeError(response["error"])

    @exchange.guard.exchange_guard
    def __send_authenticated_request(self, method, endpoint, data=None):
        timestamp = int(time.time() * 1000)

        session = requests.Session()
        request = requests.Request(method, self.api_url + endpoint)
        request.json = data

        prepared = request.prepare()
        signature_payload = \
            f'{timestamp}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._private_key.encode(), signature_payload,
                             'sha256').hexdigest()

        prepared.headers[f'FTX-KEY'] = self._public_key
        prepared.headers[f'FTX-SIGN'] = signature
        prepared.headers[f'FTX-TS'] = str(timestamp)
        prepared.headers[f'Content-type'] = 'application/json'

        response = session.send(prepared).json()

        if not response["success"]:
            raise exchange.interface.ExchangeError(response["error"])

        return response["result"]
