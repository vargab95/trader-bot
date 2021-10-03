import unittest

from config.detector import DetectorConfig, DetectorCombinationConfig
from config.common import InvalidConfigurationException


class TestDetectorConfig(unittest.TestCase):
    def setUp(self):
        self.conf = DetectorConfig({})
        self.conf.input_signal_id = "input_signal_id"
        self.conf.output_signal_id = "output_signal_id"
        self.conf.follower = False
        self.conf.follower_candle_size = 3600
        self.conf.falling_edge = False
        self.conf.stateless = False
        self.conf.latched = False
        self.conf.simple = False
        self.conf.bullish_threshold = 0.0
        self.conf.bearish_threshold = 0.0
        self.conf.reset_on_falling_edge = False

    def test_no_input_signal_specified(self):
        self.conf.input_signal_id = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_output_signal_specified(self):
        self.conf.output_signal_id = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_bearish_threshold_specified(self):
        self.conf.bearish_threshold = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_bullish_threshold_specified(self):
        self.conf.bullish_threshold = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_follower_candle_size_specified(self):
        self.conf.follower = True
        self.conf.follower_candle_size = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_dict_generation(self):
        self.assertDictEqual(self.conf.dict(), {
            "input_signal_id": "input_signal_id",
            "output_signal_id": "output_signal_id",
            "follower": False,
            "follower_candle_size": 3600,
            "falling_edge": False,
            "stateless": False,
            "latched": False,
            "simple": False,
            "bullish_threshold": 0.0,
            "bearish_threshold": 0.0,
            "reset_on_falling_edge": False
        })


class TestDetectorCombinationConfig(unittest.TestCase):
    def setUp(self):
        self.conf = DetectorCombinationConfig({})
        self.conf.input_signal_ids = ["input_signal_id"]
        self.conf.output_signal_id = "output_signal_id"
        self.conf.combination_type = "and"

    def test_no_input_signal_specified(self):
        self.conf.input_signal_ids = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_output_signal_specified(self):
        self.conf.output_signal_id = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_invalid_input_signal_specified(self):
        self.conf.input_signal_ids = "input_signal_id"
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_invalid_output_signal_specified(self):
        self.conf.output_signal_id = ["output_signal_id"]
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_combination_type(self):
        self.conf.combination_type = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_invalid_combination_type(self):
        self.conf.combination_type = "invalid"
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_dict_generation(self):
        self.assertDictEqual(self.conf.dict(), {
            "input_signal_ids": ["input_signal_id"],
            "output_signal_id": "output_signal_id",
            "combination_type": "and"
        })
