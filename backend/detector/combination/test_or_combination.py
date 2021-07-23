#!/usr/bin/python3

import unittest

from config.detector import DetectorCombinationConfig

from detector.combination.or_combination import DetectorOrCombination
from detector.common import TradingAction


class TestDetectorOrCombination(unittest.TestCase):
    @staticmethod
    def __generate_or_detector(signal_ids=None):
        if signal_ids is None:
            signal_ids = ["signal1", "signal2"]

        config = DetectorCombinationConfig({
            "input_signal_ids": signal_ids,
            "output_signal_id": "result",
            "combination_type": "or"
        })
        return DetectorOrCombination(config)

    def test_simple_or_combination_hold_or_hold(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.HOLD_SIGNAL)
        logic.update("signal2", TradingAction.HOLD_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_or_combination_hold_or_bear(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.BEARISH_SIGNAL)
        logic.update("signal2", TradingAction.HOLD_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_or_combination_bear_or_hold(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.HOLD_SIGNAL)
        logic.update("signal2", TradingAction.BEARISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_or_combination_bear_or_bear(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.BEARISH_SIGNAL)
        logic.update("signal2", TradingAction.BEARISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_or_combination_multiple_bear(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BEARISH_SIGNAL)
        logic.update("signal2", TradingAction.BEARISH_SIGNAL)
        logic.update("signal3", TradingAction.BEARISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_or_combination_multiple_bear_one_hold(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BEARISH_SIGNAL)
        logic.update("signal2", TradingAction.HOLD_SIGNAL)
        logic.update("signal3", TradingAction.BEARISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BEARISH_SIGNAL)

    def test_simple_or_combination_hold_or_bull(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.HOLD_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_or_combination_bull_or_hold(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.HOLD_SIGNAL)
        logic.update("signal2", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_or_combination_bull_or_bull(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_or_combination_multiple_bull(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.BULLISH_SIGNAL)
        logic.update("signal3", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_or_combination_multiple_bull_one_hold(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.HOLD_SIGNAL)
        logic.update("signal3", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.BULLISH_SIGNAL)

    def test_simple_or_combination_bear_or_bull(self):
        logic = self.__generate_or_detector()

        logic.update("signal1", TradingAction.BEARISH_SIGNAL)
        logic.update("signal2", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_or_combination_multiple_bull_one_bear(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.BEARISH_SIGNAL)
        logic.update("signal3", TradingAction.BULLISH_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)

    def test_simple_or_combination_one_from_all(self):
        logic = self.__generate_or_detector(["signal1", "signal2", "signal3"])

        logic.update("signal1", TradingAction.BULLISH_SIGNAL)
        logic.update("signal2", TradingAction.BEARISH_SIGNAL)
        logic.update("signal3", TradingAction.HOLD_SIGNAL)

        self.assertEqual(logic.read(), TradingAction.HOLD_SIGNAL)
