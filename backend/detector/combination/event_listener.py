#!/usr/bin/python3

from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from detector.combination.base import DetectorCombinationLogic
from detector.common import TradingAction


class DetectorCombinationEventListener(Subscriber):
    def __init__(self, output_signal_id: str, logic: DetectorCombinationLogic, publisher: Publisher):
        self.__value: TradingAction = TradingAction.HOLD_SIGNAL
        self.__logic: DetectorCombinationLogic = logic
        self.__publisher: Publisher = publisher
        self.__output_signal_id = output_signal_id

    def update(self, event: SignalUpdatedEvent):
        self.__logic.update(event.signal_name, event.value)
        self.__value = self.__logic.read()

        update_signal = SignalUpdatedEvent(self.__output_signal_id, self.__value)
        self.__publisher.notify_all_subscribers(update_signal)

    def read(self) -> TradingAction:
        return self.__value
