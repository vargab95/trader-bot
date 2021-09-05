#!/usr/bin/python3

from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from detector.common import TradingAction

from trader.base import TraderBase


class TradingActionListener(Subscriber):
    def __init__(self):
        self._value: TradingAction = TradingAction.HOLD_SIGNAL

    def update(self, event: SignalUpdatedEvent):
        if event.value == TradingAction.BEARISH_SIGNAL:
            self._value = TradingAction.BEARISH_SIGNAL
        elif event.value == TradingAction.BULLISH_SIGNAL:
            self._value = TradingAction.BULLISH_SIGNAL
        elif event.value == TradingAction.HOLD_SIGNAL:
            pass
        else:
            raise ValueError(f"{event.value} is not a valid trading action")

    def read_and_clear(self) -> TradingAction:
        value = self._value
        self._value = TradingAction.HOLD_SIGNAL
        return value


class SynchronousTradingActionListener(TradingActionListener):
    def __init__(self, trader: TraderBase):
        super().__init__()
        self.__trader: TraderBase = trader

    def update(self, event: SignalUpdatedEvent):
        super().update(event)
        self.__trader.perform(self.read_and_clear())

    def read_and_clear(self) -> TradingAction:
        value = self._value
        self._value = TradingAction.HOLD_SIGNAL
        return value
