#!/usr/bin/python3

import unittest

from config.fetcher import FetcherConfig
from observer.publisher import Publisher
from observer.subscriber import Subscriber
from observer.event import SignalUpdatedEvent

from fetcher.publisher import FetcherSignalPublisher
from fetcher.single import TradingViewFetcherSingle


class TestSubscriber(Subscriber):
    def __init__(self):
        self.value = None

    def update(self, event: SignalUpdatedEvent):
        self.value = event.value

    def get(self):
        return self.value


@unittest.mock.patch("requests.post")
class TestFilterEventListener(unittest.TestCase):
    def test_publish(self, post_mock):
        post_mock.return_value = unittest.mock.Mock()
        post_mock.return_value.json.return_value = {
            "data": [
                {"d": [1.2]}
            ]
        }

        subscriber = TestSubscriber()
        publisher = Publisher()
        config = FetcherConfig({
            "market": "BTC-USD",
            "candle_size": "1m",
            "indicator": "all",
            "check_interval": 60,
            "output_signal_id": "TestSignal"
        })
        instance = TradingViewFetcherSingle(config)
        listener = FetcherSignalPublisher(config, instance, publisher)

        publisher.register_signal(config.output_signal_id)
        publisher.subscribe(config.output_signal_id, subscriber)

        self.assertEqual(listener.read(), None)
        self.assertEqual(subscriber.get(), None)
        listener.publish()
        self.assertEqual(listener.read(), 1.2)
        self.assertAlmostEqual(subscriber.get(), 1.2)
