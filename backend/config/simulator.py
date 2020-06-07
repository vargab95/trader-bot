#!/usr/bin/python3

import typing


class SimulatorConfig:
    def __init__(self, config: typing.Dict):
        self.start_date: str = config.get("start_date", "sma")
        self.end_date: int = config.get("end_date", 2)

    def __str__(self):
        return "\nSimulator:" + \
               "\n    Start date: " + str(self.start_date) + \
               "\n    End date:   " + str(self.end_date)
