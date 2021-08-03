#!/usr/bin/python3

import unittest

from config.components import ComponentsConfig

from builder.base import TradingComponentsBuilderBase


class TestBuilderBase(unittest.TestCase):
    def test_build(self):
        config = ComponentsConfig({
            "exchanges": [{
                "id": "ftx",
                "name": "ftx",
                "private_key": "Test",
                "public_key": "Test",
                "market_name_format": "{target}-{base}"
            }],
            "fetchers": [{
                "output_signal_id": "BSV-PERP",
                "indicator_name": "BSV-PERP-IND",
                "future": True,
                "market": "BSV-PERP",
                "check_interval": 60,
                "candle_size": "1m",
                "exchange_id": "ftx",
                "type": "exchange"
            }],
            "filters": [{
                "input_signal_id": "BSV-PERP",
                "output_signal_id": "BSV-PERP-SMA",
                "type": "sma",
                "length": 12,
            }],
            "detectors": [{
                "input_signal_id": "BSV-PERP-SMA",
                "output_signal_id": "BSV-PERP-DETECTOR-2",
                "bullish_threshold": 0.0,
                "bearish_threshold": 0.0
            }, {
                "input_signal_id": "BSV-PERP-SMA",
                "output_signal_id": "BSV-PERP-DETECTOR",
                "bullish_threshold": 1.0,
                "bearish_threshold": 2.0
            }],
            "detector_combinations": [{
                "input_signal_ids": [
                    "BSV-PERP-DETECTOR",
                    "BSV-PERP-DETECTOR-2"
                ],
                "output_signal_id": "BSV-PERP-COMBINED-DETECTOR",
                "combination_type": "and"
            }],
            "traders": [{
                "input_signal_id": "BSV-PERP-COMBINED-DETECTOR"
            }]
        })

        builder = TradingComponentsBuilderBase()

        builder.build(config)

        self.assertEqual(len(builder.exchanges), 1)
        self.assertEqual(len(builder.fetchers), 1)
        self.assertEqual(len(builder.filters), 1)
        self.assertEqual(len(builder.detectors), 2)
        self.assertEqual(len(builder.detector_combinations), 1)
        self.assertEqual(len(builder.traders), 1)
