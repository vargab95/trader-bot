#!/usr/bin/python3

import logging
import typing
import enum

import config.exchange
import config.testing
import exchange.interface
import exchange.guard


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

    @property
    def profit(self):
        if self.state != TradeState.FINISHED:
            raise InvalidTradeResultRequestException
        return (self.final_price - self.entry_price) / self.entry_price * 100.0


class MockBase(exchange.interface.ExchangeInterface):
    base_coin: str = None

    def __init__(self, testing_config: config.testing.TestingConfig):
        self.__start_money = testing_config.start_money
        self._balances: exchange.interface.Balances = exchange.interface.Balances()
        self._balances[testing_config.base_asset] = self.__start_money
        MockBase.base_coin = testing_config.base_asset

        self._trade: Trade = None
        self._is_real_time: bool = testing_config.real_time
        self._fee: float = testing_config.fee
        self._client = None

        if testing_config.enabled and not self._is_real_time:
            self.price_mock: typing.Dict[str, float] = {}

    def reset(self):
        self._balances = {}
        self._balances[self.base_coin] = self.__start_money

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        logging.debug("Trying to buy %f of %s", amount, str(market))
        self._trade = Trade(market)
        price = self.get_price(market)
        if self.get_balance(market.base) >= amount * price:
            self._trade.enter(price, amount)
            self._balances[market.base] -= amount * price
            if market.target not in self._balances.keys():
                self._balances[market.target] = 0.0
            self._balances[market.target] += amount * (1 - self._fee)
            logging.info("%f %s from %s was bought for %f", amount,
                         market.target, market.base, price)
            logging.debug("New balance: %s", str(self._balances))
            return True
        logging.error("Could not complete buy %f %s for %f", amount,
                      market.base, price)
        return False

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        logging.debug("Trying to sell %f of %s", amount, str(market))
        price = self.get_price(market)
        if self.get_balance(market.target) >= amount:
            self._trade.finish(price)
            self._balances[market.target] -= amount
            self._balances[market.base] += amount * price * (1 - self._fee)
            logging.info("%f %s was sold for %f %s", amount, market.base,
                         price, market.target)
            logging.info("Trade was finished profit: %f", self._trade.profit)
            logging.debug("New balance: %s", str(self._balances))
            return True
        logging.error("Could not complete sell %f %s", amount, market.target)
        return False

    def get_balance(self, market: str) -> float:
        if market not in self._balances.keys():
            self._balances[market] = 0.0
        return self._balances[market]

    def get_balances(self) -> exchange.interface.Balances:
        return self._balances.copy()

    def get_price(self, market: exchange.interface.Market) -> float:
        return 0.0  # pragma: no cover

    def get_money(self, base: str) -> float:
        all_money: float = 0.0
        for name, balance in self._balances.items():
            if base == name:
                all_money += balance
            else:
                market = exchange.interface.Market(base, name)
                price = self.get_price(market)
                all_money += balance * price
        return all_money
