#!/usr/bin/python3

import math
import logging

import binance.client

import config.exchange
import exchange.interface


class BinanceController(exchange.interface.ExchangeInterface):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        self.client = binance.client.Client(configuration.public_key,
                                            configuration.private_key)
        exchange_info = self.client.get_exchange_info()
        self.__min_amount = {}
        logging.debug("Min quantities:")
        for market_info in exchange_info["symbols"]:
            for filter_info in market_info["filters"]:
                if filter_info["filterType"] == "LOT_SIZE":
                    min_quantity = float(filter_info["minQty"])
            symbol = market_info["symbol"]
            self.__min_amount[symbol] = min_quantity
            logging.debug("    %s: %f", symbol, min_quantity)

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self.__floor(amount, self.__min_amount[market.key])
        logging.info("Trying to buy %f %s", corrected_amount, market.key)
        logging.debug("%f was corrected to %f", amount, corrected_amount)
        try:
            self.client.create_order(
                symbol=market.key,
                side=binance.client.Client.SIDE_BUY,
                type=binance.client.Client.ORDER_TYPE_MARKET,
                quantity=str(corrected_amount))
            logging.info("%f %s was successfully bought", corrected_amount,
                         market.key)
            return True
        except binance.exceptions.BinanceAPIException as api_exception:
            logging.error("Buying %f %s was failed", corrected_amount,
                          market.key)
            logging.exception(api_exception)
            return False

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self.__floor(amount, self.__min_amount[market.key])
        logging.info("Trying to sell %f %s", corrected_amount, market.key)
        logging.debug("%f was corrected to %f", amount, corrected_amount)
        try:
            self.client.create_order(
                symbol=market.key,
                side=binance.client.Client.SIDE_SELL,
                type=binance.client.Client.ORDER_TYPE_MARKET,
                quantity=str(corrected_amount))
            logging.info("%f %s was successfully sold", corrected_amount,
                         market.key)
            return True
        except binance.exceptions.BinanceAPIException as api_exception:
            logging.error("Selling %f %s was failed", corrected_amount,
                          market.key)
            logging.exception(api_exception)
            return False

    def get_balances(self) -> exchange.interface.Balances:
        account_information = self.client.get_account()
        binance_balances = account_information["balances"]
        balances = exchange.interface.Balances()

        for balance in binance_balances:
            free = float(balance["free"])
            if free > 1e-7:
                balances[balance["asset"]] = free

        return balances

    def get_balance(self, balance: str) -> float:
        return float(self.client.get_asset_balance(asset=balance)["free"])

    def get_price(self, market: exchange.interface.Market) -> float:
        return float(self.client.get_ticker(symbol=market.key)["lastPrice"])

    def get_balances_in_different_base(
            self, base: str) -> exchange.interface.Balances:
        balances = exchange.interface.Balances()
        for name, balance in self.get_balances().items():
            if base == name:
                balances[name] = balance
            else:
                market = exchange.interface.Market(base, name)
                price = self.get_price(market)
                balances[name] = balance * price
        return balances

    def get_money(self, base: str) -> float:
        all_money: float = 0.0
        for _, balance in self.get_balances_in_different_base(base).items():
            all_money += balance
        return all_money

    @staticmethod
    def __floor(value: float, precision: float) -> float:
        exponent = -int(math.log10(precision))
        remainder = value % precision
        result = round(value, exponent)
        if remainder > (0.5 * precision):
            result -= precision
        return result
