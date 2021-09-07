#!/usr/bin/python3

import typing

from config.trader import TraderConfig
from trader.factory import TraderFactory
from trader.event_listener import SynchronousTradingActionListener

from builder.base import TradingComponentsBuilderBase


class SimulatorComponentsBuilder(TradingComponentsBuilderBase):
    def create_traders(self, trader_configs: typing.List[TraderConfig]):
        for trader_config in trader_configs:
            trader = TraderFactory.create(trader_config, self.exchanges[trader_config.exchange])
            listener = SynchronousTradingActionListener(trader)
            self.detector_signal_publisher.subscribe(trader_config.input_signal_id, listener)
            self.traders[trader_config.output_signal_id] = trader
            self.trader_listeners[trader_config.output_signal_id] = listener
