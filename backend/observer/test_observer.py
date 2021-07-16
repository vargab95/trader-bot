#!/usr/bin/python3

import unittest

from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.errors import SignalDoesNotExists, SubscriberCannotBeFound
from observer.event import ObserverEvent, SignalUpdatedEvent


class TestSubscriber(Subscriber):
    def __init__(self):
        self.update_count = 0
        self.last_event: ObserverEvent = None

    def update(self, event: ObserverEvent):
        self.update_count += 1
        self.last_event = event


class TestObserver(unittest.TestCase):
    def setUp(self):
        self.publisher = Publisher()

    def test_single_subscriber(self):
        subscriber = TestSubscriber()

        self.publisher.register_signal("TestSignal")
        self.publisher.subscribe("TestSignal", subscriber)
        self.publisher.notify_all_subscribers(SignalUpdatedEvent(signal_name="TestSignal", value=1))

        self.assertEqual(subscriber.update_count, 1)

    def test_subscribe_for_non_registered_signal(self):
        subscriber = TestSubscriber()

        with self.assertRaises(SignalDoesNotExists):
            self.publisher.subscribe("TestSignal", subscriber)

    def test_unsubscribe_single_subscriber(self):
        subscriber = TestSubscriber()

        self.publisher.register_signal("TestSignal")
        self.publisher.subscribe("TestSignal", subscriber)
        self.publisher.notify_all_subscribers(SignalUpdatedEvent(signal_name="TestSignal", value=1))
        self.publisher.unsubscribe("TestSignal", subscriber)
        self.publisher.notify_all_subscribers(SignalUpdatedEvent(signal_name="TestSignal", value=1))

        self.assertEqual(subscriber.update_count, 1)

    def test_unsubscribe_from_non_registered_signal(self):
        subscriber = TestSubscriber()

        with self.assertRaises(SignalDoesNotExists):
            self.publisher.unsubscribe("TestSignal", subscriber)

    def test_unsubscribe_non_subscribed_subscriber(self):
        subscriber = TestSubscriber()
        another_subscriber = TestSubscriber()

        self.publisher.register_signal("TestSignal")
        self.publisher.subscribe("TestSignal", subscriber)

        with self.assertRaises(SubscriberCannotBeFound):
            self.publisher.unsubscribe("TestSignal", another_subscriber)

    def create_and_notify_n_subscribers(self, number_of_subscribers=10):
        subscribers = [TestSubscriber() for _ in range(number_of_subscribers)]

        self.publisher.register_signal("TestSignal")

        for subscriber in subscribers:
            self.publisher.subscribe("TestSignal", subscriber)

        self.publisher.notify_all_subscribers(SignalUpdatedEvent("TestSignal", 1))

        return subscribers

    def test_notify_more_subscribers(self):
        subscribers = self.create_and_notify_n_subscribers()

        for subscriber in subscribers:
            self.assertEqual(subscriber.update_count, 1)

    def test_half_of_subscribers_unsubscribe(self):
        number_of_subscribers = 10
        subscribers = self.create_and_notify_n_subscribers(number_of_subscribers)

        for i in range(number_of_subscribers):
            if i % 2:
                self.publisher.unsubscribe("TestSignal", subscribers[i])

        self.publisher.notify_all_subscribers(SignalUpdatedEvent("TestSignal", 1))

        for i in range(number_of_subscribers):
            self.assertEqual(subscribers[i].update_count, 1 if i % 2 else 2)

    def test_multiple_signals(self):
        test_one_signal_subscriber = TestSubscriber()
        test_two_signal_subscriber = TestSubscriber()

        self.publisher.register_signal("TestOneSignal")
        self.publisher.register_signal("TestTwoSignal")

        self.publisher.subscribe("TestOneSignal", test_one_signal_subscriber)
        self.publisher.subscribe("TestTwoSignal", test_two_signal_subscriber)

        self.publisher.notify_all_subscribers(SignalUpdatedEvent("TestOneSignal", 1))
        self.assertEqual(test_one_signal_subscriber.update_count, 1)
        self.assertEqual(test_two_signal_subscriber.update_count, 0)

        self.publisher.notify_all_subscribers(SignalUpdatedEvent("TestTwoSignal", 1))
        self.assertEqual(test_one_signal_subscriber.update_count, 1)
        self.assertEqual(test_two_signal_subscriber.update_count, 1)

    def test_update_value(self):
        subscriber = TestSubscriber()

        self.publisher.register_signal("TestSignal")
        self.publisher.subscribe("TestSignal", subscriber)

        self.publisher.notify_all_subscribers(SignalUpdatedEvent(signal_name="TestSignal", value=1))
        self.assertEqual(subscriber.update_count, 1)
        self.assertEqual(subscriber.last_event.value, 1)

        self.publisher.notify_all_subscribers(SignalUpdatedEvent(signal_name="TestSignal", value=11))
        self.assertEqual(subscriber.update_count, 2)
        self.assertEqual(subscriber.last_event.value, 11)

    def test_notify_non_existing_signal(self):
        with self.assertRaises(SignalDoesNotExists):
            self.publisher.notify_all_subscribers(SignalUpdatedEvent("TestSignal", 1))
