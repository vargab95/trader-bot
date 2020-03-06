#!/usr/bin/python3

import exchange.interface
import exchange.mock
import exchange.controller
import config.trader

class ExchangeControllerFactory:
    @classmethod
    def create(cls, configuration: config.trader.TraderConfig) -> exchange.interface.ExchangeInterface:
        if configuration.testing.enabled:
            return exchange.mock.BinanceMock(configuration.exchange,
                                             configuration.testing)
        return exchange.controller.BinanceController(configuration.exchange)
