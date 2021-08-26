#!/usr/bin/python3

import abc
import logging
import typing
import enum

import config.exchange
import config.testing
import exchange.interface
from exchange.interface import Market
import exchange.guard

from signals.trading_signal import TradingSignal, TickerSignalDescriptor


class TradeState(enum.Enum):
    NOT_STARTED = 0
    ON_GOING = 1
    FINISHED = 2


class InvalidTradeResultRequestException(Exception):
    pass


class Trade:
    def __init__(self, market: exchange.interface.Market):
        self.market: exchange.interface.Market = market
        self.entry_price: float = None
        self.final_price: float = None
        self.amount: float = None
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

    def __init__(self, exchange_config: config.exchange.ExchangeConfig):
        self.__start_money = exchange_config.start_money
        self._configuration = exchange_config
        self._balances: exchange.interface.Balances = exchange.interface.Balances()
        self._balances[exchange_config.base_asset] = self.__start_money
        self._positions: exchange.interface.Balances = exchange.interface.Balances()
        self._future_loans: exchange.interface.Balances = exchange.interface.Balances()
        MockBase.base_coin = exchange_config.base_asset

        self._is_real_time: bool = False
        self.set_real_time(self._configuration.real_time)

        self._fee: float = exchange_config.fee
        self._client = None
        self._precision = exchange_config.balance_precision
        self._real_exchange: exchange.interface.ExchangeInterface = None

        if not self._is_real_time:
            self.price_mock: typing.Dict[str, float] = {}
            self.leverage: float = 1.0

    def get_market_key(self, market: Market) -> str:
        return market.key(name_format=self._configuration.market_name_format)

    @abc.abstractmethod
    def set_real_time(self, real_time: bool) -> None:
        pass  # pragma: no cover

    def reset(self):
        self._balances = exchange.interface.Balances()
        self._balances[self.base_coin] = self.__start_money
        self._positions = exchange.interface.Balances()
        self._future_loans = exchange.interface.Balances()

    def bet_on_bearish(self, market: Market, amount: float) -> bool:
        return self.__handle_future_bet(market, amount, False)

    def bet_on_bullish(self, market: Market, amount: float) -> bool:
        return self.__handle_future_bet(market, amount, True)

    def __handle_future_bet(self, market: Market, amount: float, is_bullish: bool) -> bool:
        position = self.get_position(market)
        to_sell = 0

        if position < 0 if is_bullish else position > 0:
            diff = abs(position) - amount
            to_sell = diff if diff > 0 else amount
            self.__handle_future_sell(market, to_sell, not is_bullish)
            amount -= to_sell

            if amount <= 0:
                return True
        return self.__handle_future_purchase(market, amount, is_bullish)

    def __handle_future_purchase(self, market: Market, amount: float, is_bullish: bool) -> bool:
        if amount <= 0.0:
            return False

        amount = self._floor(amount, self._precision)
        price = self.get_price(market)
        leveraged_amount = amount * price / self.leverage
        market_key = self.get_market_key(market)
        if self.get_leverage_balance() >= leveraged_amount:
            self._balances[self.base_coin] -= leveraged_amount
            self._positions[market_key] += ((amount * (1 - self._fee)) * (1 if is_bullish else -1))

            if market_key not in self._future_loans.keys():
                self._future_loans[market_key] = 0.0
            self._future_loans[market_key] += (amount * price) - leveraged_amount

            return True
        return False

    def __handle_future_sell(self, market: Market, amount: float, is_bullish: bool) -> None:
        amount = self._floor(amount, self._precision)
        price = self.get_price(market)
        market_key = self.get_market_key(market)
        self._positions[market_key] += -amount if is_bullish else amount
        self._balances[self.base_coin] += abs(amount) * price * (1 - self._fee)

    def close_position(self, market: Market) -> bool:
        super().close_position(market)
        market_key = self.get_market_key(market)
        self._balances[self.base_coin] -= self._future_loans[market_key]
        if self._balances[self.base_coin] < 0:
            raise exchange.interface.ExchangeError("Future position has liquidated!!!")
        return True

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        logging.debug("Amount to buy: %f", amount)
        amount = self._floor(amount, self._precision)
        logging.debug("Amount was rounded to %f", amount)
        logging.info("Trying to buy %f of %s", amount, str(market))
        price = self.get_price(market)
        if self.get_balance(market.base) >= amount * price:
            self._balances[market.base] -= amount * price
            if market.target not in self._balances.keys():
                self._balances[market.target] = 0.0
            self._balances[market.target] += amount * (1 - self._fee)
            logging.info("%f %s from %s was bought for %f", amount,
                         market.target, market.base, price)
            logging.debug("New balance: %s", str(self._balances))
            return True
        logging.error("Could not complete buy %f %s for %f", amount,
                      market.target, price)
        logging.debug("Amount to buy in %s: %f", market.base, amount * price)
        logging.debug("Balance in %s: %f", market.base,
                      self.get_balance(market.base))
        return False

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        if amount <= 0:
            logging.error("Trying to sell 0 or less amount")
            return False

        logging.debug("Amount to sell: %f", amount)
        amount = self._floor(amount, self._precision)
        logging.debug("Amount was rounded to %f", amount)
        logging.info("Trying to sell %f of %s", amount, str(market))
        price = self.get_price(market)
        if self.get_balance(market.target) >= amount:
            self._balances[market.target] -= amount
            self._balances[market.base] += amount * price * (1 - self._fee)
            logging.info("%f %s was sold for %f %s", amount, market.target,
                         price, market.base)
            logging.debug("New balance: %s", str(self._balances))
            return True

        logging.error("Could not complete sell %f %s", amount, market.target)
        logging.debug("Amount to sell in %s: %f", market.base, amount * price)
        logging.debug("Balance in %s: %f", market.base,
                      self.get_balance(market.base))
        return False

    def get_balance(self, market: str) -> float:
        if market not in self._balances.keys():
            self._balances[market] = 0.0
        return self._balances[market]

    def get_leverage_balance(self) -> float:
        balances: exchange.interface.Balances = self.get_balances()
        return balances[self.base_coin] * self.leverage

    def get_balances(self) -> exchange.interface.Balances:
        return self._balances.copy()

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "price", future: bool = False) -> float:
        if self._is_real_time:
            return self._real_exchange.get_price(market, keyword, future)
        return self.price_mock[self.get_market_key(market)]

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        if self._is_real_time:
            return self._real_exchange.get_price_history(descriptor, keyword)
        raise NotImplementedError("Mocked price history has not been implemented yet")

    def get_positions(self) -> exchange.interface.Balances:
        return self._positions.copy()

    def get_position(self, market: exchange.interface.Market) -> float:
        market_key = self.get_market_key(market)
        if market_key not in self._positions.keys():
            self._positions[market_key] = 0.0
        return self._positions[market_key]

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
