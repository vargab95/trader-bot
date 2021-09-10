#!/usr/bin/python3

import logging
import json
import copy

from builder.simulator import SimulatorComponentsBuilder
from exchange.interface import ExchangeInterface
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent
from fetcher.common import CannotFetchDataException
from detector.common import TradingAction

from applications.base import ApplicationBase


class PriceMockUpdater(Subscriber):
    def __init__(self, market_key: str, exchange: ExchangeInterface):
        self.__exchange: ExchangeInterface = exchange
        self.__market_key: str = market_key

    def update(self, event: SignalUpdatedEvent):
        self.__exchange.price_mock[self.__market_key] = event.value


class ExecutionLogSubscriber(Subscriber):
    def __init__(self, builder: SimulatorComponentsBuilder):
        self.__execution_log = list()
        self.__builder: SimulatorComponentsBuilder = builder

    def update(self, event: SignalUpdatedEvent):
        signals_to_write = dict()

        for name, exchange in self.__builder.exchanges.items():
            signals_to_write[name + "-PRICE-MOCK"] = copy.deepcopy(exchange.price_mock)
            signals_to_write[name + "-BALANCES"] = exchange.get_balances()
            signals_to_write[name + "-POSITIONS"] = exchange.get_positions()
            signals_to_write[name + "-FUTURE-LOANS"] = exchange._future_loans

        for name, fetcher in self.__builder.fetchers.items():
            signals_to_write[name + "-TIMESTAMP"] = fetcher.get_timestamp()
            signals_to_write[name] = fetcher.get_technical_indicator()

        for name, filter_ in self.__builder.filters.items():
            signals_to_write[name] = filter_.get()

        for name, detector in self.__builder.detectors.items():
            signals_to_write[name] = str(detector.read())

        for name, detector_combination in self.__builder.detector_combinations.items():
            signals_to_write[name] = str(detector_combination.read())

        for name, trader in self.__builder.traders.items():
            signals_to_write[name] = str(trader.state)

        self.__execution_log.append(signals_to_write)

    def write_to_file(self, path: str):
        with open(path, "w") as log_file:
            json.dump(self.__execution_log, log_file, indent=2)


class SimulatorApplication(ApplicationBase):
    def __init__(self):
        super().__init__()
        self._builder: SimulatorComponentsBuilder = SimulatorComponentsBuilder()
        self.__execution_log_writer: ExecutionLogSubscriber = None

    def _initialize_application_logic(self):
        self._builder.build(self._configuration.components, self._configuration.testing.enabled)
        for signal_id in self._builder.fetcher_publishers:
            for exchange in self._builder.exchanges.values():
                updater = PriceMockUpdater(signal_id, exchange)
                self._builder.analogue_signal_publisher.subscribe(signal_id, updater)

        if self._configuration.simulator.log_output_path:
            self.__execution_log_writer = ExecutionLogSubscriber(self._builder)

            for signal_id in self._builder.analogue_signal_publisher.signals:
                self._builder.analogue_signal_publisher.subscribe(signal_id, self.__execution_log_writer)

            for signal_id in self._builder.detector_signal_publisher.signals:
                self._builder.detector_signal_publisher.subscribe(signal_id, self.__execution_log_writer)

    def _run_application_logic(self):
        try:
            while True:
                for fetcher_publisher in self._builder.fetcher_publishers.values():
                    fetcher_publisher.publish()
        except CannotFetchDataException:
            logging.info("Data stream ended.")

        for name, trader in self._builder.traders.items():
            trader.perform(TradingAction.RETURN_TO_BASE_SIGNAL)

        if self.__execution_log_writer:
            self.__execution_log_writer.write_to_file(self._configuration.simulator.log_output_path)

        for name, exchange in self._builder.exchanges.items():
            print(f"Exchange {name}:")
            print("    Balances:", exchange.get_balances())
            print("    Positions:", exchange.get_positions())
            print("    Prices:", exchange.price_mock)
