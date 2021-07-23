#!/usr/bin/python3

import logging
import config.trader
import trader.leverage.simple
import trader.leverage.stepped
import trader.single.simple
import trader.future.simple
import exchange.interface


class InvalidTradingMethod(Exception):
    pass


class TraderFactory:
    @staticmethod
    def create(configuration: config.trader.TraderConfig, used_exchange: exchange.interface.ExchangeInterface):
        if configuration.leverage:
            if configuration.method == "simple":
                logging.info("SimpleLeverageTrader was instantiated")
                return trader.leverage.simple.SimpleLeverageTrader(configuration, used_exchange)

            if configuration.method == "stepped":
                logging.info("SteppedLeverageTrader was instantiated")
                return trader.leverage.stepped.SteppedLeverageTrader(configuration, used_exchange)
        elif configuration.future:
            logging.info("SimpleFutureTrader was instantiated")
            return trader.future.simple.SimpleFutureTrader(configuration, used_exchange)
        else:
            if configuration.method == "simple":
                logging.info("SimpleSingleMarketTrader was instantiated")
                return trader.single.simple.SimpleSingleMarketTrader(configuration, used_exchange)

        raise InvalidTradingMethod()
