#!/usr/bin/python3

import exchange.interface
import exchange.binance_mock
import exchange.ftx
import exchange.ftx_mock
import exchange.binance
import config.exchange


class ExchangeControllerFactory:
    @classmethod
    def create(cls, configuration: config.exchange.ExchangeConfig, testing: bool = False):
        if configuration.name == "ftx":
            if testing:
                return exchange.ftx_mock.FtxMock(configuration)
            return exchange.ftx.FtxController(configuration)
        if configuration.testing.enabled:
            return exchange.binance_mock.BinanceMock(configuration)
        return exchange.binance.BinanceController(configuration)
