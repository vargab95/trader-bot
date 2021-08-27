#!/usr/bin/python3

import unittest

from filters.event_listener import FilterEventListener
from filters.sma import SMA
from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from config.filter import FilterConfig


class TestSubscriber(Subscriber):
    def __init__(self):
        self.value = None

    def update(self, event: SignalUpdatedEvent):
        self.value = event.value

    def get(self):
        return self.value


class TestFilterEventListener(unittest.TestCase):
    def test_event_listener_update(self):
        subscriber = TestSubscriber()
        publisher = Publisher()
        filter_instance = SMA(FilterConfig({"length": 2}))
        output_signal_id = "TestSignal"
        listener = FilterEventListener(output_signal_id, filter_instance, publisher)

        publisher.register_signal(output_signal_id)
        publisher.subscribe(output_signal_id, subscriber)

        listener.update(SignalUpdatedEvent("InputSignal", 1.0))
        self.assertEqual(subscriber.get(), None)
        self.assertEqual(listener.read(), None)

        listener.update(SignalUpdatedEvent("InputSignal", 2.0))
        self.assertAlmostEqual(subscriber.get(), 1.5)
        self.assertEqual(listener.read(), 1.5)
