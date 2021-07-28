#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class GathererConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.exchange_id: str = config.get("exchange_id", "ftx")
        self.input_signal_ids: typing.List[str] = config.get("input_signal_ids", None)

    def __str__(self):
        return "\nGatherer:" + \
               "\n    Exchange id:             " + str(self.exchange_id)

    def validate(self):
        pass
