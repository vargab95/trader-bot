#!/usr/bin/python3

import unittest
import unittest.mock
import datetime
import binance.client

from config.exchange import ExchangeConfig
import exchange.factory
import exchange.interface
import signals.trading_signal


@unittest.mock.patch("exchange.binance.binance.client.Client")
class BinanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config: ExchangeConfig = ExchangeConfig({})
        cls.config.name = "binance"
        cls.config.public_key = "test_pub_key"
        cls.config.private_key = "test_prv_key"
        cls.config.market_name_format = "{target}{base}"
        exchange.interface.Market.name_format = cls.config.market_name_format

    def test_buy(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 5
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 3
                        }
                    ]
                }
            ]
        }
        handle.get_ticker.return_value = {"lastPrice": 1}

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        controller.buy(market, 5)

        handle.create_order.assert_called_once_with(symbol=market.key(self.config.market_name_format),
                                                    quantity='5.',
                                                    side=binance.client.Client.SIDE_BUY,
                                                    type=binance.client.Client.ORDER_TYPE_MARKET)

    def test_buy_rounding(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 0.0001
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 0.001
                        }
                    ]
                }
            ]
        }
        handle.get_ticker.return_value = {"lastPrice": 1}

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        controller.buy(market, 1.23456789)

        handle.create_order.assert_called_once_with(symbol=market.key(self.config.market_name_format),
                                                    quantity='1.2345',
                                                    side=binance.client.Client.SIDE_BUY,
                                                    type=binance.client.Client.ORDER_TYPE_MARKET)

    def test_buy_round_to_zero(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 0.0001
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 0.001
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, 0.0000123)

    def test_buy_below_notional(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_ticker.return_value = {"lastPrice": 1.0}
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 0.0000001
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 0.001
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, 0.0000123)

    def test_sell(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 5
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 3
                        }
                    ]
                }
            ]
        }
        handle.get_ticker.return_value = {"lastPrice": 1}

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        controller.sell(market, 5)

        handle.create_order.assert_called_once_with(
            symbol=market.key(self.config.market_name_format),
            quantity='5.',
            side=binance.client.Client.SIDE_SELL,
            type=binance.client.Client.ORDER_TYPE_MARKET)

    def test_sell_round_to_zero(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 0.0001
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 0.001
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.sell(market, 0.0000123)

    def test_buy_negative(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 5
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 3
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, -5)

    def test_sell_negative(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 5
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 3
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.sell(market, -5)

    def test_buy_not_enough_quantity(self, mock_client):
        market = exchange.interface.Market("ETH", "BTC")
        handle = mock_client()
        handle.create_order.return_value = True
        handle.get_exchange_info.return_value = {
            "symbols": [
                {
                    "symbol": market.key(self.config.market_name_format),
                    "filters": [
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": 5000
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": 3
                        }
                    ]
                }
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        with self.assertRaises(exchange.interface.ZeroOrNegativeAmountError):
            controller.buy(market, 5)

    def test_get_balances(self, mock_client):
        handle = mock_client()
        handle.get_account.return_value = {
            "balances": [
                {"asset": "BTC", "free": 10.0},
                {"asset": "ETH", "free": 20.0}
            ]
        }

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        self.assertEqual(controller.get_balances(), {"ETH": 20.0, "BTC": 10.0})

        handle.get_account.assert_called_once()

    def test_get_balance(self, mock_client):
        handle = mock_client()
        handle.get_asset_balance.return_value = {"free": 20.0}

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        self.assertAlmostEqual(controller.get_balance("ETH"), 20.0)

        handle.get_asset_balance.assert_called_once_with(asset="ETH")

    def test_get_price(self, mock_client):
        handle = mock_client()
        handle.get_ticker.return_value = {"lastPrice": 20.0}
        market = exchange.interface.Market("ETH", "BTC")

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        self.assertAlmostEqual(controller.get_price(market), 20.0)

        handle.get_ticker.assert_called_once_with(symbol=market.key(self.config.market_name_format))

    def test_get_money(self, mock_client):
        handle = mock_client()
        handle.get_account.return_value = {
            "balances": [
                {"asset": "BTC", "free": 10.0},
                {"asset": "ETH", "free": 20.0}
            ]
        }
        handle.get_ticker.return_value = {"lastPrice": 1}

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        self.assertEqual(controller.get_money("BTC"), 30.0)

        handle.get_account.assert_called_once()
        handle.get_ticker.assert_called_with(symbol='ETHBTC')

    def test_historical_price(self, mock_client):
        handle = mock_client()
        handle.get_historical_klines.return_value = [
            [
                1499040000000,
                "0.01634790",
                "0.80000000",
                "0.01575800",
                "0.01577100",
                "148976.11427815",
                1499644799999,
                "2434.19055334",
                308,
                "1756.87402397",
                "28.46694368",
                "17928899.62484339"
            ]
        ]

        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)

        market = exchange.interface.Market("USD", "BTC")

        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, None, None, 50, 1, datetime.timedelta(seconds=60))

        self.assertListEqual(controller.get_price_history(descriptor).data,
                             [signals.trading_signal.TradingSignalPoint(
                              value=0.015771, date=datetime.datetime(2017, 7, 3, 2, 0))])

        handle.get_historical_klines.assert_called_once()

    def test_historical_price_invalid_resolution(self, _):
        controller = exchange.factory.ExchangeControllerFactory.create(self.config, testing=False)
        market = exchange.interface.Market("USD", "BTC")

        descriptor = signals.trading_signal.TickerSignalDescriptor(
            market, None, None, 50, 1, datetime.timedelta(seconds=65))

        with self.assertRaises(ValueError):
            controller.get_price_history(descriptor)
