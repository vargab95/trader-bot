#!/usr/bin/python3

import abc
import typing
import logging

import detector.common

import trader.base
from trader.common import TraderState, BEARISH_STATES, BULLISH_STATES
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

    def _sell(self, market: exchange.interface.Market, _: float = 1.0) -> None:
        try:
            position = self._exchange.get_position(market)
            should_close = False

            if self.state in BULLISH_STATES and position > 0:
                should_close = True
            elif self.state in BEARISH_STATES and position < 0:
                should_close = True

            if should_close:
                self._exchange.close_position(market)
        except exchange.interface.ZeroOrNegativeAmountError:
            pass

    def _buy(self, market: exchange.interface.Market, ratio: float = 1.0) -> None:
        base_asset = self._configuration.future_base_asset
        balance = self._exchange.get_leverage_balance()
        price = self._exchange.get_price(market,
                                         self._configuration.bullish_price_keyword,
                                         self._configuration.future)
        amount = balance / price * ratio
        logging.debug("Base asset: %s, balance: %f, price: %f, amount: %f", base_asset, balance, price, amount)

        last_exception = None
        for _ in range(10):
            try:
                if self._state == TraderState.BUYING_BEARISH:
                    logging.info("%f of %s was sold to go to bearish position", amount, str(market))
                    self._exchange.bet_on_bearish(market, amount)
                elif self._state == TraderState.BUYING_BULLISH:
                    logging.info("%f of %s was bought to go to bullish position", amount, str(market))
                    self._exchange.bet_on_bullish(market, amount)
                return
            except exchange.interface.ExchangeError as exc:
                last_exception = exc
            amount *= 0.99

        if last_exception:
            raise last_exception

    def _detect_and_set_start_state(self):
        position = self._exchange.get_position(self._configuration.market)
        if position > 0:
            self._state = TraderState.BULLISH
        elif position < 0:
            self._state = TraderState.BEARISH
        else:
            self._state = TraderState.BASE
