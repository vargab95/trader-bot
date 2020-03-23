#!/usr/bin/python3

import typing


class TestingConfig:
    def __init__(self, config: typing.Dict):
        self.enabled: bool = config.get("enabled", False)
        self.real_time: bool = config.get("real_time", False)
        self.start_money: float = config.get("start_money", 100.0)
        self.fee: float = config.get("fee", 0.001)
        self.balance_store: str = config.get("balance_store", "balances.json")

    def __str__(self):
        return "\nTesting:" + \
               "\n    Enabled:        " + str(self.enabled) + \
               "\n    Real time:      " + str(self.real_time) + \
               "\n    Fee:            " + str(self.fee) + \
               "\n    Balances store: " + self.balance_store + \
               "\n    Start money:    " + str(self.start_money)