#!/usr/bin/python3

import typing

from config.logging import LoggingConfig
from config.testing import TestingConfig
from config.exchange import ExchangeConfig
from config.mail import MailConfig
from config.database import DatabaseConfig
from config.server import ServerConfig
from config.simulator import SimulatorConfig
from config.components import ComponentsConfig


class ApplicationConfig:
    def __init__(self, config: typing.Dict = None):
        self.logging = LoggingConfig(config.get("logging", {}))
        self.testing = TestingConfig(config.get("testing", {}))
        self.exchange = ExchangeConfig(config.get("exchange", {}))
        self.mail = MailConfig(config.get("mail", {}))
        self.database = DatabaseConfig(config.get("database", {}))
        self.server = ServerConfig(config.get("server", {}))
        self.simulator = SimulatorConfig(config.get("simulator", {}))
        self.components = ComponentsConfig(config.get("components", {}))

    def __str__(self):
        return ''.join(
            [str(attribute) for attribute in self.__dict__.values()])
