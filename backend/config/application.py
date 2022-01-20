#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.logging import LoggingConfig
from config.testing import TestingConfig
from config.mail import MailConfig
from config.database import DatabaseConfig
from config.server import ServerConfig
from config.simulator import SimulatorConfig
from config.components import ComponentsConfig
from config.gatherer import GathererConfig


class ApplicationConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict = None):
        # Reserved for later use if configuration migration feature
        # would be necessary
        self.configuration_version = "1.0.0"

        # Sections for subcomponents
        self.logging = LoggingConfig(config.get("logging", {}))
        self.testing = TestingConfig(config.get("testing", {}))
        self.mail = MailConfig(config.get("mail", {}))
        self.database = DatabaseConfig(config.get("database", {}))
        self.server = ServerConfig(config.get("server", {}))
        self.gatherer = GathererConfig(config.get("gatherer", {}))
        self.simulator = SimulatorConfig(config.get("simulator", {}))
        self.components = ComponentsConfig(config.get("components", {}))

    def validate(self):
        for attribute in self.__dict__.values():
            if not isinstance(attribute, str):
                attribute.validate()
