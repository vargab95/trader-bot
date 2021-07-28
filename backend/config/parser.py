#!/usr/bin/python3

import logging
import yaml

from config.application import ApplicationConfig
from config.common import InvalidConfigurationException


class ConfigurationParser:
    def __init__(self):
        self.configuration: ApplicationConfig = None

    def read(self, path):
        try:
            with open(path, "r") as config_file:
                configuration = yaml.safe_load(config_file)
                print(configuration)
        except (FileNotFoundError, yaml.constructor.ConstructorError) as exception:
            logging.error(
                "Exception occured during parsing configuration: %s",
                str(exception))
            raise InvalidConfigurationException from exception
        self.configuration = ApplicationConfig(configuration)
        print(self.configuration.dict())
