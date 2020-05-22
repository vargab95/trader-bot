#!/usr/bin/python3

import config.application
import traders.leverage.simple
import traders.leverage.stepped
import exchange.interface


class InvalidTradingMethod(Exception):
    pass


class TraderFactory:
    @staticmethod
    def create(configuration: config.application.ApplicationConfig,
               used_exchange: exchange.interface.ExchangeInterface):
        if configuration.trader.method == "simple":
            return traders.leverage.simple.SimpleLeverageTrader(
                configuration, used_exchange)

        if configuration.trader.method == "stepped":
            return traders.leverage.stepped.SteppedLeverageTrader(
                configuration, used_exchange)

        raise InvalidTradingMethod()
