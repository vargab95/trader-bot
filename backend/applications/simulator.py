#!/usr/bin/python3

import sys
import csv
import datetime
import logging

import applications.base
import trader.base
import trader.factory
import filters.base
import filters.factory

from signals.trading_signal import TradingSignalPoint


class SimulatorApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__trader: trader.base.TraderBase
        self.__filter: filters.base.Filter
        self.__all_money_history = []
        self.__last_money = 0.0
        self.__input = {}

    def _initialize_application_logic(self):
        # self._initialize_client()
        # self._initialize_storages()
        self._initialize_exchange()
        self.__trader = trader.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()
        self.__filter = filters.factory.FilterFactory.create_complex(
            self._configuration.filter)
        self.__read_input_file(
            self._configuration.simulator.watched_file_path,
            self._configuration.exchange.watched_market.key)
        self.__read_input_file(
            self._configuration.simulator.bullish_file_path,
            self._configuration.exchange.bullish_market.key)
        self.__read_input_file(
            self._configuration.simulator.bearish_file_path,
            self._configuration.exchange.bearish_market.key)
        self.__validate_input()

    def _run_application_logic(self):
        simulator_input = self.__input[self._configuration.exchange.watched_market.key]
        for i, signal_point in enumerate(simulator_input):
            logging.debug("Simulating date %s",
                          signal_point.date.strftime("%Y:%m:%d %H:%M:%S"))
            self.__fill_price_mocks(i)
            self.__filter.put(signal_point.value)
            if self.__filter.get() is not None:
                self.__trader.perform(self.__filter.get())

            self.__all_money_history.append(self._exchange.get_money(
                self._configuration.exchange.watched_market.base))
            self.__last_money = self.__all_money_history[-1]
        print(self.__all_money_history)

    def __validate_input(self):
        input_lengths = [len(input) for input in self.__input.values()]
        if not all(x == input_lengths[0] for x in input_lengths):
            logging.critical("Inputs have different lengths")
            sys.exit(1)

        for i in range(len(list(self.__input.values())[0])):
            all_dates_in_line = [
                input[i].date for input in self.__input.values()]
            if not all(x == all_dates_in_line[0] for x in all_dates_in_line):
                logging.critical("Inputs have different dates")
                sys.exit(1)

    def __read_input_file(self, path, key):
        self.__input[key] = []
        with open(path, "r") as csvfile:
            logging.debug("Loading %s", path)
            data = csv.reader(csvfile, delimiter=";")
            for line in data:
                self.__input[key].append(TradingSignalPoint(
                    value=float(line[1]), date=datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S+00:00')))
            logging.debug("%s was loaded successfully", path)

    def __fill_price_mocks(self, i):
        for key, signal_points in self.__input.items():
            self._exchange.price_mock[key] = signal_points[i].value
