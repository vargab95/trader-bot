#!/usr/bin/python3

import logging

import binance.client

import config.exchange
import exchange.base
import exchange.interface
import exchange.guard


class BinanceController(exchange.base.ExchangeBase):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        super().__init__(configuration)
        self.client = binance.client.Client(self._public_key,
                                            self._private_key)
        exchange_info = self.client.get_exchange_info()
        logging.debug("Min quantities:")
        for market_info in exchange_info["symbols"]:
            for filter_info in market_info["filters"]:
                if filter_info["filterType"] == "LOT_SIZE":
                    min_quantity = float(filter_info["minQty"])
                if filter_info["filterType"] == "MIN_NOTIONAL":
                    min_notional = float(filter_info["minNotional"])
            symbol = market_info["symbol"]
            self._min_amount[symbol] = min_quantity
            self._min_notional[symbol] = min_notional
            logging.debug("    %s: LOT_SIZE: %f MIN_NOTIONAL: %f", symbol,
                          min_quantity, min_notional)

    @exchange.guard.exchange_guard
    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self._check_and_log_corrected_amount(
            market, amount, "buy")

        if corrected_amount <= 0.0:
            return False

        self.client.create_order(
            symbol=market.key,
            side=binance.client.Client.SIDE_BUY,
            type=binance.client.Client.ORDER_TYPE_MARKET,
            quantity="{:.12f}".format(corrected_amount).rstrip('0'))
        logging.info("%.10f %s was successfully bought", corrected_amount,
                     market.key)
        return True

    @exchange.guard.exchange_guard
    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        corrected_amount = self._check_and_log_corrected_amount(
            market, amount, "sell")

        if corrected_amount <= 0.0:
            return False

        self.client.create_order(
            symbol=market.key,
            side=binance.client.Client.SIDE_SELL,
            type=binance.client.Client.ORDER_TYPE_MARKET,
            quantity="{:.12f}".format(corrected_amount).rstrip('0'))
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
    def get_balance(self, market: str) -> float:
        return float(self.client.get_asset_balance(asset=market)["free"])

    @exchange.guard.exchange_guard
    def get_price(self, market: exchange.interface.Market) -> float:
        return float(self.client.get_ticker(symbol=market.key)["lastPrice"])
