#!/usr/bin/python3

from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from detector.common import TradingAction


class TradingActionListener(Subscriber):
    def __init__(self):
        self.__value: TradingAction = TradingAction.HOLD_SIGNAL

    def update(self, event: SignalUpdatedEvent):
        if event.value == TradingAction.BEARISH_SIGNAL:
            self.__value = TradingAction.BEARISH_SIGNAL
        elif event.value == TradingAction.BULLISH_SIGNAL:
            self.__value = TradingAction.BULLISH_SIGNAL
        elif event.value == TradingAction.HOLD_SIGNAL:
            pass
        else:
            raise ValueError(f"{event.value} is not a valid trading action")

    def read_and_clear(self) -> TradingAction:
        value = self.__value
        self.__value = TradingAction.HOLD_SIGNAL
        return value
