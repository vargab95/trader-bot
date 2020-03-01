#!/usr/bin/python3

import logging
import typing
import enum

import binance

import config
import exchange.interface

class TradeState(enum.Enum):
    NOT_STARTED = 0
    ON_GOING = 1
    FINISHED = 2

class InvalidTradeResultRequestException(Exception):
    pass

class Trade:
    def __init__(self, market: exchange.interface.Market):
        self.market: exchange.interface.Market = market
        self.entry_price: float = 0.0
        self.final_price: float = 0.0
        self.amount: float = 0.0
        self.state: TradeState = TradeState.NOT_STARTED

    def enter(self, price: float, amount: float):
        self.entry_price = price
        self.amount = amount
        self.state = TradeState.ON_GOING

    def finish(self, price: float):
        self.final_price = price
        self.state = TradeState.FINISHED

    def reset(self):
        self.entry_price = 0.0
        self.final_price = 0.0
        self.amount = 0.0
        self.state = TradeState.NOT_STARTED

    @property
    def profit(self):
        if self.state != TradeState.FINISHED:
            raise InvalidTradeResultRequestException
        return (self.final_price - self.entry_price) * self.amount

class BinanceMock(exchange.interface.ExchangeInterface):
    base_coin = "USDT"

    def __init__(self,
                 exchange_config: config.ExchangeConfig,
                 testing_config: config.TestingConfig):
        self.__balances: typing.Dict[str, float] = {}
        self.__balances["USDT"] = testing_config.start_money

        self.__trade: Trade = None
        self.__is_real_time: bool = testing_config.real_time

        if testing_config.enabled and not self.__is_real_time:
            self.price_mock: typing.Dict[str, float] = {}
        else:
            self.__client = binance.client.Client(exchange_config.public_key, exchange_config.private_key)

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        self.__trade = Trade(market)
        price = self.get_price(market)
        if self.__balances[market.base] >= amount * price:
            self.__trade.enter(price, amount)
            self.__balances[market.base] -= amount * price
            if market.target not in self.__balances.keys():
                self.__balances[market.target] = 0.0
            self.__balances[market.target] += amount
            logging.info("%f %s from %s was bought for %f", amount, market.target, market.base, price)
            return True
        return False

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        price = self.get_price(market)
        if self.__balances[market.target] >= amount:
            self.__trade.finish(price)
            self.__balances[market.target] -= amount
            self.__balances[market.base] += amount * price
            logging.info("%f %s was sold for %f %s", amount, market.base, market.target, price)
            logging.info("Trade was finished profit: %f", self.__trade.profit)
            return True
        return False

    def get_balances(self) -> exchange.interface.Balances:
        return self.__balances

    def get_price(self, market: exchange.interface.Market):
        if self.__is_real_time:
            return float(self.__client.get_ticker(symbol=market.key)["lastPrice"])
        return self.price_mock[market.key]

    def __handle_balance_change(self, market: exchange.interface.Market, trade: Trade):
        pass
