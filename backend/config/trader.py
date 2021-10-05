#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException
from exchange.interface import Market

from trader.common import TraderState


class TraderConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.input_signal_id = config.get("input_signal_id", None)
        self.output_signal_id = config.get("output_signal_id", None)
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)

        state_str = config.get("start_state", "auto")
        self.start_state = None
        self.auto_detect_start_state = False
        if state_str == "base":
            self.start_state = TraderState.BASE
        elif state_str == "bull":
            self.start_state = TraderState.BULLISH
        elif state_str == "bear":
            self.start_state = TraderState.BEARISH
        elif state_str == "auto":
            self.auto_detect_start_state = True

        self.max_steps = config.get("max_steps", 5)
        self.future = bool(config.get("future", False))
        self.future_base_asset = config.get("future_base_asset", "USD")

        if config.get("market", False):
            self.market: Market = Market.create_from_string(config.get("market", "BTC-USDT"))
            self.bearish_market: Market = self.market
            self.bullish_market: Market = self.market
        else:
            self.bearish_market: Market = Market.create_from_string(config.get("bearish_market", "BEAR-USDT"))
            self.bullish_market: Market = Market.create_from_string(config.get("bullish_market", "BULL-USDT"))

        self.default_price_keyword = config.get("default_price_keyword", "price")
        self.bullish_price_keyword = config.get("bullish_price_keyword", "price")
        self.bearish_price_keyword = config.get("bearish_price_keyword", "price")
        self.exchange = config.get("exchange", "ftx")

    def validate(self):
        if self.input_signal_id is None:
            raise InvalidConfigurationException("Input signal id is a mandatory parameter for traders")

        if self.output_signal_id is None:
            raise InvalidConfigurationException("Output signal id is a mandatory parameter for traders")

        if not self.auto_detect_start_state and self.start_state is None:
            raise InvalidConfigurationException("Invalid start state in trader config")

        if self.auto_detect_start_state and self.start_state is not None:
            raise InvalidConfigurationException("Invalid start state in trader config")
