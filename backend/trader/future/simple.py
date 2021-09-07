#!/usr/bin/python3

from exchange.interface import ExchangeError

import trader.future.base
import trader.common

from trader.common import TraderState


class SimpleFutureTrader(trader.future.base.FutureTraderBase):
    def _bullish_logic(self):
        if self._state != TraderState.BULLISH:
            if self._state != TraderState.BASE:
                try:
                    self._sell(self._configuration.market)
                    self._state = TraderState.BUYING_BULLISH
                except ExchangeError:
                    self._state = TraderState.SELLING_BEARISH
                    raise
            else:
                self._state = TraderState.BUYING_BULLISH

            if self._state == TraderState.BUYING_BULLISH:
                self._buy(self._configuration.market)
                self._state = TraderState.BULLISH

    def _bearish_logic(self):
        if self._state != TraderState.BEARISH:
            if self._state != TraderState.BASE:
                try:
                    self._sell(self._configuration.market)
                    self._state = TraderState.BUYING_BEARISH
                except ExchangeError:
                    self._state = TraderState.SELLING_BULLISH
                    raise
            else:
                self._state = TraderState.BUYING_BEARISH
            if self._state == TraderState.BUYING_BEARISH:
                self._buy(self._configuration.market)
                self._state = TraderState.BEARISH

    def _return_to_base_logic(self):
        if self._state in [TraderState.BULLISH, TraderState.SELLING_BULLISH, TraderState.BUYING_BULLISH]:
            try:
                self._sell(self._configuration.market)
                self._state = TraderState.BASE
            except ExchangeError:
                self._state = TraderState.SELLING_BULLISH
                raise
        elif self._state in [TraderState.BEARISH, TraderState.SELLING_BEARISH, TraderState.BUYING_BEARISH]:
            try:
                self._sell(self._configuration.market)
                self._state = TraderState.BASE
            except ExchangeError:
                self._state = TraderState.SELLING_BEARISH
                raise
