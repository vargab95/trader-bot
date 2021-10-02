#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class SimulatorConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.bullish_file_path: str = config.get("bullish_file_path", None)
        self.bearish_file_path: str = config.get("bearish_file_path", None)
        self.watched_file_path: str = config.get("watched_file_path", None)
        self.log_output_path: str = config.get("log_output_path", None)
        self.actions_output_path: str = config.get("actions_output_path", None)

    def validate(self):
        pass
