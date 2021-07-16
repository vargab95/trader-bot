#!/usr/bin/python3

import abc
import typing
import logging

import detector.common

import trader.base
from trader.common import TraderState
import exchange.interface


class FutureTraderBase(trader.base.TraderBase):
    @abc.abstractmethod
    def _bullish_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _bearish_logic(self):  # pragma: no cover
        pass

    def _bullish_condition(self, action: typing.List[detector.common.TradingAction]):
        return detector.common.TradingAction.BULLISH_SIGNAL == action

    def _bearish_condition(self, action: detector.common.TradingAction):
        return detector.common.TradingAction.BEARISH_SIGNAL == action

    def _sell(self,
              market: exchange.interface.Market,
              ratio: float = 1.0) -> bool:
        position = self._exchange.get_position(market)
        logging.info("[Future-Sell] Position: %f", position)
        if position > 0.0:
            logging.info("%s was on position %f so bullish position was sold",
                         market.key, position)
            return self._exchange.sell(market, position)
        if position < 0.0:
            logging.info("%s was on position %f so bearish position was sold",
                         market.key, position)
            return self._exchange.buy(market, -position)
        return False

    def _buy(self,
             market: exchange.interface.Market,
             ratio: float = 1.0) -> bool:
        base_asset = self._configuration.exchange.future_base_asset
        balance = self._exchange.get_leverage_balance()
        price = self._exchange.get_price(market, self._configuration.exchange.bullish_price_keyword)
        amount = balance / price * ratio
        logging.debug("Base asset: %s, balance: %f, price: %f, amount: %f", base_asset, balance, price, amount)

        for _ in range(10):
            if self._state == TraderState.BUYING_BEARISH:
                logging.info("%f of %s was sold to go to bearish position",
                             amount, market.key)
                result = self._exchange.sell(market, amount)
            elif self._state == TraderState.BUYING_BULLISH:
                logging.info("%f of %s was bought to go to bullish position",
                             amount, market.key)
                result = self._exchange.buy(market, amount)
            if result:
                return True
            amount *= 0.99
        return False
