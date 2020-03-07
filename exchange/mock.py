#!/usr/bin/python3

import logging
import typing
import enum

import binance

import config.exchange
import config.testing
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
        return (self.final_price - self.entry_price) / self.entry_price * 100.0


class BinanceMock(exchange.interface.ExchangeInterface):
    base_coin = "USDT"

    def __init__(self, exchange_config: config.exchange.ExchangeConfig,
                 testing_config: config.testing.TestingConfig):
        self.__balances: typing.Dict[str, float] = {}
        self.__balances["USDT"] = testing_config.start_money

        self.__trade: Trade = None
        self.__is_real_time: bool = testing_config.real_time
        self.__fee: float = testing_config.fee

        if testing_config.enabled and not self.__is_real_time:
            self.price_mock: typing.Dict[str, float] = {}
        else:
            self.__client = binance.client.Client(exchange_config.public_key,
                                                  exchange_config.private_key)

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        logging.debug("Trying to buy %f of %s", amount, str(market))
        self.__trade = Trade(market)
        price = self.get_price(market)
        if self.__balances[market.base] >= amount * price:
            self.__trade.enter(price, amount)
            self.__balances[market.base] -= amount * price
            if market.target not in self.__balances.keys():
                self.__balances[market.target] = 0.0
            self.__balances[market.target] += amount * (1 - self.__fee)
            logging.info("%f %s from %s was bought for %f", amount,
                         market.target, market.base, price)
            return True
        logging.error("Could not complete buy %f %s for %f", amount,
                      market.base, price)
        return False

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        logging.debug("Trying to sell %f of %s", amount, str(market))
        price = self.get_price(market)
        if self.__balances[market.target] >= amount:
            self.__trade.finish(price)
            self.__balances[market.target] -= amount
            self.__balances[market.base] += amount * price * (1 - self.__fee)
            logging.info("%f %s was sold for %f %s", amount, market.base,
                         price, market.target)
            logging.info("Trade was finished profit: %f", self.__trade.profit)
            return True
        logging.error("Could not complete sell %f %s", amount, market.target)
        return False

    def get_balance(self, balance: str) -> float:
        if balance not in self.__balances.keys():
            self.__balances[balance] = 0.0
        return self.__balances[balance]

    def get_balances(self) -> exchange.interface.Balances:
        return self.__balances.copy()

    def get_price(self, market: exchange.interface.Market) -> float:
        if self.__is_real_time:
            return float(
                self.__client.get_ticker(symbol=market.key)["lastPrice"])
        return self.price_mock[market.key]

    def get_money(self, base: str) -> float:
        all_money: float = 0.0
        for name, balance in self.__balances.items():
            if base == name:
                all_money += balance
            else:
                market = exchange.interface.Market(base, name)
                price = self.get_price(market)
                all_money += balance * price
        return all_money
