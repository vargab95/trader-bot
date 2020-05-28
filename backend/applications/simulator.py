#!/usr/bin/python3

import logging

import applications.base
import trader.base
import trader.factory
import filters.base


class SimulatorApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__trader: trader.base.TraderBase
        self.__filter: filters.base.Filter
        self.__all_money_history = []

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()
        self.__trader = trader.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()

    def _run_application_logic(self):
        simulator_input = []
        for indicator in simulator_input:
            self.__filter.put(indicator)
            if self.__filter.get():
                self.__trader.perform(indicator)

            self.__all_money_history.append(self._exchange.get_money(
                self._configuration.exchange.watched_market.base))
