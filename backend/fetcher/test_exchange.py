#!/usr/bin/python3

import unittest

from config.fetcher import FetcherConfig
from config.exchange import ExchangeConfig
from exchange.ftx_mock import FtxMock

from fetcher.exchange import ExchangeFetcher


class TestExchangeFetcher(unittest.TestCase):
    def test_fetched_value(self):
        exchange = FtxMock(ExchangeConfig({
            "id": "ftx",
            "name": "ftx",
            "real_time": False
        }))
        fetcher = ExchangeFetcher(
            FetcherConfig({
                "indicator_name": "BSV-PERP",
                "market": "BSV-PERP",
                "check_interval": 60
            }),
            exchange
        )

        exchange.price_mock["BSV-PERP"] = 10.0

        fetcher.fetch_technical_indicator()
        self.assertAlmostEqual(fetcher.get_technical_indicator(), 10.0)

