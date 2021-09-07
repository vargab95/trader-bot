#!/usr/bin/python3

import json

from builder.simulator import SimulatorComponentsBuilder
from exchange.interface import ExchangeInterface
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent
from fetcher.common import CannotFetchDataException

from applications.base import ApplicationBase


class PriceMockUpdater(Subscriber):
    def __init__(self, market_key: str, exchange: ExchangeInterface):
        self.__exchange: ExchangeInterface = exchange
        self.__market_key: str = market_key

    def update(self, event: SignalUpdatedEvent):
        self.__exchange.price_mock[self.__market_key] = event.value


class SimulatorApplication(ApplicationBase):
    def __init__(self):
        super().__init__()
        self._builder: SimulatorComponentsBuilder = SimulatorComponentsBuilder()

    def _initialize_application_logic(self):
        self._builder.build(self._configuration.components, self._configuration.testing.enabled)
        for signal_id in self._builder.fetcher_publishers:
            for exchange in self._builder.exchanges.values():
                updater = PriceMockUpdater(signal_id, exchange)
                self._builder.analogue_signal_publisher.subscribe(signal_id, updater)

    def _run_application_logic(self):
        execution_log = list()

        try:
            while True:
                for fetcher_publisher in self._builder.fetcher_publishers.values():
                    fetcher_publisher.publish()

                    if self._configuration.simulator.log_output_path:
                        signals_to_write = dict()

                        for name, fetcher in self._builder.fetchers.items():
                            signals_to_write[name + "-TIMESTAMP"] = fetcher.get_timestamp()
                            signals_to_write[name] = fetcher.get_technical_indicator()

                        for name, filter_ in self._builder.filters.items():
                            signals_to_write[name] = filter_.get()

                        for name, detector in self._builder.detectors.items():
                            signals_to_write[name] = str(detector.read())

                        for name, detector_combination in self._builder.detector_combinations.items():
                            signals_to_write[name] = str(detector_combination.read())

                        for name, trader in self._builder.traders.items():
                            signals_to_write[name] = str(trader.state)

                        execution_log.append(signals_to_write)
        except CannotFetchDataException:
            pass

        if self._configuration.simulator.log_output_path:
            with open(self._configuration.simulator.log_output_path, "w") as log_file:
                json.dump(execution_log, log_file, indent=2)

        for name, exchange in self._builder.exchanges.items():
            print(f"Exchange {name}:")
            print("    Balances:", exchange.get_balances())
            print("    Positions:", exchange.get_positions())
            print("    Prices:", exchange.price_mock)
