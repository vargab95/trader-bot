#!/usr/bin/python3

import unittest

from config.detector import DetectorCombinationConfig
from detector.combination.event_listener import DetectorCombinationEventListener
from detector.combination.and_combination import DetectorAndCombination
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


class TestDetectorCombinationEventListener(unittest.TestCase):
    def test_event_listener_update(self):
        subscriber = TestSubscriber()
        publisher = Publisher()
        output_signal_id = "TestSignal"
        logic = DetectorAndCombination(DetectorCombinationConfig({
            "input_signal_ids": ["InputSignal1", "InputSignal2"],
            "output_signal_id": output_signal_id
        }))
        listener = DetectorCombinationEventListener(output_signal_id, logic, publisher)

        publisher.register_signal(output_signal_id)
        publisher.subscribe(output_signal_id, subscriber)

        listener.update(SignalUpdatedEvent("InputSignal1", TradingAction.BULLISH_SIGNAL))
        self.assertEqual(subscriber.get(), TradingAction.HOLD_SIGNAL)
        self.assertEqual(listener.read(), TradingAction.HOLD_SIGNAL)

        listener.update(SignalUpdatedEvent("InputSignal2", TradingAction.BULLISH_SIGNAL))
        self.assertEqual(subscriber.get(), TradingAction.BULLISH_SIGNAL)
        self.assertEqual(listener.read(), TradingAction.BULLISH_SIGNAL)


if __name__ == "__main__":
    unittest.main()
