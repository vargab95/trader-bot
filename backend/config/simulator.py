#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class SimulatorConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.bullish_file_path: str = config.get("bullish_file_path", "")
        self.bearish_file_path: str = config.get("bearish_file_path", "")
        self.watched_file_path: str = config.get("watched_file_path", "")
        self.log_output_path: str = config.get(
            "log_output_path", "simulator_log.csv")
        self.actions_output_path: str = config.get(
            "actions_output_path", "simulator_actions.csv")

    def __str__(self):
        return "\nSimulator:" + \
               "\n    Bullish data file:   " + str(self.bullish_file_path) + \
               "\n    Bearish data file:   " + str(self.bearish_file_path) + \
               "\n    Watched data file:   " + str(self.watched_file_path) + \
               "\n    Log output path:     " + str(self.log_output_path) + \
               "\n    Actions output path: " + str(self.actions_output_path)
