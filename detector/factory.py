#!/usr/bin/python3

import detector.interface
import config

class DetectorFactory:
    @classmethod
    def create(cls, configuration: config.MarketConfig) -> detector.interface.ExchangeInterface:
        if configuration.testing.enabled:
            return exchange.mock.BinanceMock(configuration.exchange,
                                             configuration.testing)
        return exchange.controller.BinanceController(configuration.exchange)
