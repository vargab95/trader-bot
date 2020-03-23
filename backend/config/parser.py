#!/usr/bin/python3

import yaml

from config.trader import TraderConfig


class ConfigurationParser:
    def __init__(self):
        self.configuration: TraderConfig = None

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            self.configuration = TraderConfig(configuration)
