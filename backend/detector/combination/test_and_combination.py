#!/usr/bin/python3

import unittest

from config.detector import DetectorCombinationConfig
from observer.publisher import Publisher
from observer.event import SignalUpdatedEvent

from detector.combination.and_combination import DetectorAndCombination
from detector.common import TradingAction


class TestDetectorAndCombination(unittest.TestCase):
    def setUp(self):
        self.publisher = Publisher()
        self.publisher.register_signal("result")

    def __generate_and_detector(self, signal_ids=None):
        if signal_ids is None:
            signal_ids = ["signal1", "signal2"]

        config = DetectorCombinationConfig({
            "input_signal_ids": signal_ids,
            "output_signal_id": "result",
            "combination_type": "and"
        })
        return DetectorAndCombination(config, self.publisher)

    def test_simple_and_combination_hold_and_hold(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.HOLD_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.HOLD_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_hold_and_bear(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.HOLD_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_bear_and_hold(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.HOLD_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BEARISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_bear_and_bear(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BEARISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_and_combination_multiple_bear(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.BEARISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_and_combination_multiple_bear_one_hold(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.HOLD_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.BEARISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_hold_and_bull(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.HOLD_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_bull_and_hold(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.HOLD_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_bull_and_bull(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_and_combination_multiple_bull(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_and_combination_multiple_bull_one_hold(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.HOLD_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_bear_and_bull(self):
        logic = self.__generate_and_detector()

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_multiple_bull_one_bear(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.BULLISH_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_and_combination_one_from_all(self):
        logic = self.__generate_and_detector(["signal1", "signal2", "signal3"])

        logic.update(SignalUpdatedEvent("signal1", TradingAction.BULLISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal2", TradingAction.BEARISH_SIGNAL))
        logic.update(SignalUpdatedEvent("signal3", TradingAction.HOLD_SIGNAL))

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)
