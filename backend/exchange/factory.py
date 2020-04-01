#!/usr/bin/python3

import exchange.interface
import exchange.binance_mock
import exchange.binance
import config.trader


class ExchangeControllerFactory:
    @classmethod
    def create(
        cls, configuration: config.trader.TraderConfig
    ) -> exchange.interface.ExchangeInterface:
        if configuration.testing.enabled:
            return exchange.binance_mock.BinanceMock(configuration.exchange,
                                                     configuration.testing)
        return exchange.binance.BinanceController(configuration.exchange)
