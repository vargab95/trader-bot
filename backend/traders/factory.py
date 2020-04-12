#!/usr/bin/python3

import config.trader
import traders.leverage.simple
import traders.leverage.stepped
import exchange.interface


class InvalidTradingMethod(Exception):
    pass


class TraderFactory:
    @staticmethod
    def create(configuration: config.trader.TraderConfig,
               used_exchange: exchange.interface.ExchangeInterface):
        if configuration.market.method == "simple":
            return traders.leverage.simple.SimpleLeverageTrader(
                configuration, used_exchange)

        if configuration.market.method == "stepped":
            return traders.leverage.stepped.SteppedLeverageTrader(
                configuration, used_exchange)

        raise InvalidTradingMethod()
