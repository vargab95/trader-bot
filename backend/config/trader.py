#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException
from exchange.interface import Market

from trader.common import TraderState


class TraderConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.input_signal_id = config.get("input_signal_id", None)
        self.indicator = config.get("indicator", "all")
        self.check_interval = config.get("check_interval", 60)
        self.candle_size = config.get("candle_size", "1h")
        self.method = config.get("method", "simple")
        self.leverage = config.get("leverage", False)

        state_str = config.get("start_state", "base")
        if state_str == "base":
            self.start_state = TraderState.BASE
        elif state_str == "bull":
            self.start_state = TraderState.BULLISH
        elif state_str == "bear":
            self.start_state = TraderState.BEARISH
        else:
            self.start_state = None

        self.max_steps = config.get("max_steps", 5)
        self.initial_values = config.get("initial_values", [])
        self.initial_length = config.get("initial_length", 1)
        self.initial_keyword = config.get("initial_keyword", "close")
        self.initial_step = config.get("initial_step", 1)
        self.future = bool(config.get("future", False))
        self.future_base_asset = config.get("future_base_asset", "USD")
        self.market: Market = Market.create_from_string(config.get("market", "BTC-USDT"))
        self.bearish_market: Market = Market.create_from_string(config.get("bearish_market", "BEAR-USDT"))
        self.bullish_market: Market = Market.create_from_string(config.get("bullish_market", "BULL-USDT"))
        self.default_price_keyword = config.get("default_price_keyword", "price")
        self.bullish_price_keyword = config.get("bullish_price_keyword", "price")
        self.bearish_price_keyword = config.get("bearish_price_keyword", "price")
        self.exchange = config.get("exchange", "ftx")

    def __str__(self):
        return "\nTrader:" + \
               "\n    Input signal id:             " + str(self.input_signal_id) + \
               "\n    Market:                      " + str(self.market) + \
               "\n    Indicator:                   " + str(self.indicator) + \
               "\n    Candle size:                 " + str(self.candle_size) + \
               "\n    Method:                      " + str(self.method) + \
               "\n    Leverage:                    " + str(self.leverage) + \
               "\n    Start state:                 " + str(self.start_state) + \
               "\n    Step count:                  " + str(self.max_steps) + \
               "\n    Check interval:              " + str(self.check_interval) + \
               "\n    Future:                      " + str(self.future) + \
               "\n    Initialization list length:  " + str(self.initial_length) + \
               "\n    Initialization list keyword: " + str(self.initial_keyword)

    def validate(self):
        if self.input_signal_id is None:
            raise InvalidConfigurationException("Input signal id is a mandatory parameter for traders")

        if self.start_state is None:
            raise InvalidConfigurationException("Invalid start state in trader config")
