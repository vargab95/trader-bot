#!/usr/bin/python3

import exchange.interface
import exchange.mock_base
from exchange.ftx import FtxController


class FtxMock(exchange.mock_base.MockBase):
    def set_real_time(self, real_time: bool) -> None:
        self._is_real_time = real_time

        if self._is_real_time and self._real_exchange is None:
            self._real_exchange = FtxController(self._configuration)
