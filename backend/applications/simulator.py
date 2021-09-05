#!/usr/bin/python3

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
        try:
            while True:
                for fetcher_publisher in self._builder.fetcher_publishers.values():
                    fetcher_publisher.publish()
        except CannotFetchDataException:
            pass
