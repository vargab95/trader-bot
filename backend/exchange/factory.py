#!/usr/bin/python3

import exchange.interface
import exchange.binance_mock
import exchange.ftx
import exchange.ftx_mock
import exchange.binance
import config.application


class ExchangeControllerFactory:
    @classmethod
    def create(cls, configuration: config.application.ApplicationConfig):
        if configuration.exchange.name == "ftx":
            if configuration.testing.enabled:
                return exchange.ftx_mock.FtxMock(configuration.exchange,
                                                 configuration.testing)
            return exchange.ftx.FtxController(configuration.exchange)
        if configuration.testing.enabled:
            return exchange.binance_mock.BinanceMock(configuration.exchange,
                                                     configuration.testing)
        return exchange.binance.BinanceController(configuration.exchange)
