#!/usr/bin/python3

import exchange.interface
import exchange.mock
import exchange.controller

class ExchangeControllerFactory:
    @classmethod
    def create(cls, testing: bool) -> exchange.interface.ExchangeInterface:
        if testing:
            return exchange.mock.BinanceMock()
        return exchange.controller.BinanceController()
