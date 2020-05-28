#!/usr/bin/python3

import logging

import applications.base
import trader.base
import trader.factory
import filters.base
import filters.factory


class SimulatorApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__trader: trader.base.TraderBase
        self.__filter: filters.base.Filter
        self.__all_money_history = []

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()
        self._initialize_exchange()
        self.__trader = trader.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()
        self.__filter = filters.factory.FilterFactory.create_complex(
            self._configuration.filter)

    def _run_application_logic(self):
        simulator_input = self._ticker_storage.get(
            self._configuration.trader.market, limit=1000000)
        for indicator in simulator_input:
            self._exchange.price_mock["BULLUSDT"] = indicator["price"]
            self._exchange.price_mock["BEARUSDT"] = indicator["price"]
            self._exchange.price_mock["BTCUSDT"] = indicator["price"]
            self.__filter.put(indicator["price"])
            if self.__filter.get():
                self.__trader.perform(self.__filter.get())

            self.__all_money_history.append(self._exchange.get_money(
                self._configuration.exchange.watched_market.base))
            self.__last_money = self.__all_money_history[-1]
        print(self.__all_money_history)
