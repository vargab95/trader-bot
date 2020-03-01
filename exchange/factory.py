#!/usr/bin/python3

import exchange.interface
import exchange.mock
import exchange.controller
import config

class ExchangeControllerFactory:
    @classmethod
    def create(cls, configuration: config.TraderConfig) -> exchange.interface.ExchangeInterface:
        if configuration.testing.enabled:
            return exchange.mock.BinanceMock(configuration.exchange,
                                             configuration.testing)
        return exchange.controller.BinanceController(configuration.exchange)
