#!/usr/bin/python3

import yaml

from config.application import ApplicationConfig


class ConfigurationParser:
    def __init__(self):
        self.configuration: ApplicationConfig = None

    def read(self, path):
        with open(path, "r") as config_file:
            configuration = yaml.safe_load(config_file)
            self.configuration = ApplicationConfig(configuration)
