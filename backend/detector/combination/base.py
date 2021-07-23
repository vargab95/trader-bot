#!/usr/bin/python3

import abc
import typing

from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent
from config.detector import DetectorCombinationConfig

from detector.common import TradingAction


class DetectorCombinationLogic(Subscriber):
    def __init__(self, config: DetectorCombinationConfig, publisher: Publisher):
        self.__config = config
        self.__last_signals: typing.Dict[str, TradingAction] = dict()
        self.__result: TradingAction = TradingAction.HOLD_SIGNAL
        self.__publisher: Publisher = publisher

    def update(self, event: SignalUpdatedEvent):
        self.__last_signals[event.signal_name] = event.value

        if len(self.__config.input_signal_ids) != len(self.__last_signals):
            return

        self.__result = self._calculate(self.__last_signals)

        update_event = SignalUpdatedEvent(self.__config.output_signal_id, self.__result)
        self.__publisher.notify_all_subscribers(update_event)

    @abc.abstractmethod
    def _calculate(self, signals: typing.Dict[str, TradingAction]) -> TradingAction:
        pass

    def read(self) -> TradingAction:
        return self.__result
