#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase


class SimulatorConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        # Path of simulator event logging
        self.log_output_path: str = config.get("log_output_path", None)

    def validate(self):
        pass
