#!/usr/bin/python3

import unittest

from detector.event_listener import DetectorEventListener
from detector.rising_edge import RisingEdgeDetector
from detector.common import TradingAction
from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent


class TestSubscriber(Subscriber):
    def __init__(self):
        self.value = None

    def update(self, event: SignalUpdatedEvent):
        self.value = event.value

    def get(self):
        return self.value


class TestDetectorEventListener(unittest.TestCase):
    def test_event_listener_update(self):
        subscriber = TestSubscriber()
        publisher = Publisher()
        output_signal_id = "TestSignal"
        logic = RisingEdgeDetector(0.0, 0.0)
        listener = DetectorEventListener(output_signal_id, logic, publisher)

        publisher.register_signal(output_signal_id)
        publisher.subscribe(output_signal_id, subscriber)

        listener.update(SignalUpdatedEvent("InputSignal", 0.0))
        self.assertEqual(subscriber.get(), TradingAction.HOLD_SIGNAL)
        self.assertEqual(listener.read(), TradingAction.HOLD_SIGNAL)

        listener.update(SignalUpdatedEvent("InputSignal", 0.1))
        self.assertEqual(subscriber.get(), TradingAction.BULLISH_SIGNAL)
        self.assertEqual(listener.read(), TradingAction.BULLISH_SIGNAL)


if __name__ == "__main__":
    unittest.main()
