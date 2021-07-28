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
        self.logging = LoggingConfig(config.get("logging", {}))
        self.testing = TestingConfig(config.get("testing", {}))
        self.mail = MailConfig(config.get("mail", {}))
        self.database = DatabaseConfig(config.get("database", {}))
        self.server = ServerConfig(config.get("server", {}))
        self.gatherer = GathererConfig(config.get("gatherer", {}))
        self.simulator = SimulatorConfig(config.get("simulator", {}))
        self.components = ComponentsConfig(config.get("components", {}))
