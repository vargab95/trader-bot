#!/usr/bin/python3

import config.trader
import traders.leverage.simple
import exchange.interface


class TraderFactory:
    @staticmethod
    def create(configuration: config.trader.TraderConfig,
               used_exchange: exchange.interface.ExchangeInterface):
        return traders.leverage.simple.SimpleLeverageTrader(
            configuration, used_exchange)
