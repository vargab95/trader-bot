#!/usr/bin/python3

import math
import logging

import binance.client

import config.exchange
import exchange.interface
import exchange.guard


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

    @exchange.guard.exchange_guard
    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self.__floor(amount, self.__min_amount[market.key])
        logging.info("Trying to buy %.10f %s", corrected_amount, market.key)
        logging.debug("%.10f was corrected to %.10f", amount, corrected_amount)

        if corrected_amount < self.__min_amount[market.key]:
            logging.warning("Buy failed due to insufficient resources.")
            return False

        self.client.create_order(symbol=market.key,
                                 side=binance.client.Client.SIDE_BUY,
                                 type=binance.client.Client.ORDER_TYPE_MARKET,
                                 quantity=str(corrected_amount))
        logging.info("%.10f %s was successfully bought", corrected_amount,
                     market.key)
        return True

    @exchange.guard.exchange_guard
    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self.__floor(amount, self.__min_amount[market.key])
        logging.info("Trying to sell %.10f %s", corrected_amount, market.key)
        logging.debug("%.10f was corrected to %.10f", amount, corrected_amount)

        if corrected_amount < self.__min_amount[market.key]:
            logging.warning("Sell failed due to insufficient resources.")
            return False

        self.client.create_order(symbol=market.key,
                                 side=binance.client.Client.SIDE_SELL,
                                 type=binance.client.Client.ORDER_TYPE_MARKET,
                                 quantity=str(corrected_amount))
        logging.info("%.10f %s was successfully sold", corrected_amount,
                     market.key)
        return True

    @exchange.guard.exchange_guard
    def get_balances(self) -> exchange.interface.Balances:
        account_information = self.client.get_account()
        binance_balances = account_information["balances"]
        balances = exchange.interface.Balances()

        for balance in binance_balances:
            free = float(balance["free"])
            if free > 1e-7:
                balances[balance["asset"]] = free

        return balances

    @exchange.guard.exchange_guard
    def get_balance(self, balance: str) -> float:
        return float(self.client.get_asset_balance(asset=balance)["free"])

    @exchange.guard.exchange_guard
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
        result = value
        if remainder > (0.5 * precision):
            result -= precision
        result = round(result, exponent)
        return result
