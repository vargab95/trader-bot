#!/usr/bin/python3

import logging

import config.exchange
import exchange.interface
import exchange.guard
from exchange.interface import Market

from signals.trading_signal import TradingSignal, TickerSignalDescriptor


class ExchangeBase(exchange.interface.ExchangeInterface):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        self._configuration = configuration
        self._public_key = configuration.public_key
        self._private_key = configuration.private_key
        self._min_amount = dict()
        self._min_notional = dict()

    def get_market_key(self, market: Market) -> str:
        return market.key(name_format=self._configuration.market_name_format)

    def _is_enough_amount(self, market, amount: float):
        if amount < self._min_amount[self.get_market_key(market)]:
            return False

        price = self.get_price(market)
        if amount < (self._min_notional[self.get_market_key(market)] / price):
            return False

        return True

    def _get_balances_in_different_base(
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

    def _check_and_log_corrected_amount(self, market, amount, operation):
        corrected_amount = self._floor(amount, self._min_amount[self.get_market_key(market)])
        logging.info("Trying to %s %.10f %s", operation, corrected_amount,
                     self.get_market_key(market))
        logging.debug("%.10f was corrected to %.10f", amount, corrected_amount)

        if not self._is_enough_amount(market, corrected_amount):
            logging.warning("%s failed due to insufficient resources.",
                            operation)
            return 0.0

        corrected_amount_str = "{:.12f}".format(corrected_amount).rstrip('0')
        logging.debug("Corrected amount string: %s", corrected_amount_str)
        return corrected_amount

    def get_money(self, base: str) -> float:
        all_money: float = 0.0
        logging.debug("Calculating all money for %s", base)
        for _, balance in self._get_balances_in_different_base(base).items():
            all_money += balance
        return all_money

    def bet_on_bearish(self, market: Market, amount: float) -> bool:
        raise NotImplementedError  # pragma: no cover

    def bet_on_bullish(self, market: Market, amount: float) -> bool:
        raise NotImplementedError  # pragma: no cover

    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        raise NotImplementedError  # pragma: no cover

    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        raise NotImplementedError  # pragma: no cover

    def get_balances(self) -> exchange.interface.Balances:
        raise NotImplementedError  # pragma: no cover

    def get_balance(self, market: str) -> float:
        raise NotImplementedError  # pragma: no cover

    def get_positions(self) -> exchange.interface.Balances:
        raise NotImplementedError  # pragma: no cover

    def get_position(self, market: exchange.interface.Market) -> float:
        raise NotImplementedError  # pragma: no cover

    def get_leverage_balance(self) -> float:
        raise NotImplementedError  # pragma: no cover

    def get_price(self, market: exchange.interface.Market, keyword: str = "price", future: bool = False) -> float:
        return -1.0  # pragma: no cover

    def get_price_history(self, descriptor: TickerSignalDescriptor) -> TradingSignal:
        pass  # pragma: no cover
