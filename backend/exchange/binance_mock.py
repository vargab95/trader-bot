#!/usr/bin/python3

import exchange.interface
import exchange.mock_base
from exchange.binance import BinanceController


class BinanceMock(exchange.mock_base.MockBase):
    def set_real_time(self, real_time: bool) -> None:
        self._is_real_time = real_time

        if self._is_real_time and self._real_exchange is None:
            self._real_exchange = BinanceController(self._configuration)
