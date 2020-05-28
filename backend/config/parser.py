#!/usr/bin/python3

import logging
import yaml

from config.application import ApplicationConfig
from config.common import InvalidConfigurationException


class ConfigurationParser:
    def __init__(self):
        self.configuration: ApplicationConfig = None

    def read(self, path):
        with open(path, "r") as config_file:
            try:
                configuration = yaml.safe_load(config_file)
            except yaml.constructor.ConstructorError as exception:
                logging.error(
                    "Exception occured during parsing configuration: %s",
                    str(exception))
                raise InvalidConfigurationException
            self.configuration = ApplicationConfig(configuration)
