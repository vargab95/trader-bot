#!/usr/bin/python3

import config.application
import trader.leverage.simple
import trader.leverage.stepped
import trader.single.simple
import trader.future.simple
import exchange.interface


class InvalidTradingMethod(Exception):
    pass


class TraderFactory:
    @staticmethod
    def create(configuration: config.application.ApplicationConfig,
               used_exchange: exchange.interface.ExchangeInterface):
        if configuration.trader.leverage:
            if configuration.trader.method == "simple":
                return trader.leverage.simple.SimpleLeverageTrader(configuration, used_exchange)

            if configuration.trader.method == "stepped":
                return trader.leverage.stepped.SteppedLeverageTrader(configuration, used_exchange)
        elif configuration.exchange.future:
            return trader.future.simple.SimpleFutureTrader(configuration, used_exchange)
        else:
            if configuration.trader.method == "simple":
                return trader.single.simple.SimpleSingleMarketTrader(configuration, used_exchange)

        raise InvalidTradingMethod()
