#!/usr/bin/python3

import unittest

from config.detector import DetectorCombinationConfig
from observer.publisher import Publisher
from observer.event import SignalUpdatedEvent

from detector.combination.not_combination import DetectorNotCombination
from detector.common import TradingAction


class TestDetectorNotCombination(unittest.TestCase):
    def setUp(self):
        self.publisher = Publisher()
        self.publisher.register_signal("result")

    def __generate_not_detector(self, signal_ids=None):
        config = DetectorCombinationConfig({
            "input_signal_ids": ["signal"],
            "output_signal_id": "result",
            "combination_type": "not"
        })
        return DetectorNotCombination(config, self.publisher)

    def test_simple_not_combination_hold(self):
        logic = self.__generate_not_detector()

        logic.update(SignalUpdatedEvent("signal", TradingAction.HOLD_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_not_combination_bear(self):
        logic = self.__generate_not_detector()

        logic.update(SignalUpdatedEvent("signal", TradingAction.BEARISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_not_combination_bull(self):
        logic = self.__generate_not_detector()

        logic.update(SignalUpdatedEvent("signal", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)
