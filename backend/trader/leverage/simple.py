#!/usr/bin/python3

from exchange.interface import ExchangeError

import trader.leverage.base
import trader.common

from trader.common import TraderState


class SimpleLeverageTrader(trader.leverage.base.LeverageTraderBase):
    def _bullish_logic(self):
        if self._state != TraderState.BULLISH:
            if self._state != TraderState.BASE and self._state != TraderState.BUYING_BULLISH:
                try:
                    self._sell(self._configuration.bearish_market)
                    self._state = TraderState.BUYING_BULLISH
                except ExchangeError:
                    self._state = TraderState.SELLING_BEARISH
                    raise
            else:
                self._state = TraderState.BUYING_BULLISH

            if self._state == TraderState.BUYING_BULLISH:
                self._buy(self._configuration.bullish_market)
                self._state = TraderState.BULLISH

    def _bearish_logic(self):
        if self._state != TraderState.BEARISH:
            if self._state != TraderState.BASE and self._state != TraderState.BUYING_BEARISH:
                try:
                    self._sell(self._configuration.bullish_market)
                    self._state = TraderState.BUYING_BEARISH
                except ExchangeError:
                    self._state = TraderState.SELLING_BULLISH
                    raise
            else:
                self._state = TraderState.BUYING_BEARISH

            if self._state == TraderState.BUYING_BEARISH:
                self._buy(self._configuration.bearish_market)
                self._state = TraderState.BEARISH

    def _return_to_base_logic(self):
        if self._state == TraderState.BEARISH or self._state == TraderState.SELLING_BEARISH:
            try:
                self._sell(self._configuration.bearish_market)
                self._state = TraderState.BASE
            except ExchangeError:
                self._state = TraderState.SELLING_BEARISH
                raise
        elif self._state == TraderState.BULLISH or self._state == TraderState.SELLING_BULLISH:
            try:
                self._sell(self._configuration.bullish_market)
                self._state = TraderState.BASE
            except ExchangeError:
                self._state = TraderState.SELLING_BULLISH
                raise
