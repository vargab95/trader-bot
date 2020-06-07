#!/usr/bin/python3

import typing

from config.logging import LoggingConfig
from config.testing import TestingConfig
from config.trader import TraderConfig
from config.exchange import ExchangeConfig
from config.mail import MailConfig
from config.database import DatabaseConfig
from config.server import ServerConfig
from config.filter import FilterConfig


class ApplicationConfig:
    def __init__(self, configuration: typing.Dict = None):
        self.logging = LoggingConfig(configuration.get("logging", {}))
        self.testing = TestingConfig(configuration.get("testing", {}))
        self.trader = TraderConfig(configuration.get("trader", {}))
        self.exchange = ExchangeConfig(configuration.get("exchange", {}))
        self.mail = MailConfig(configuration.get("mail", {}))
        self.database = DatabaseConfig(configuration.get("database", {}))
        self.server = ServerConfig(configuration.get("server", {}))
        self.filter = [FilterConfig(filter_element)
                       for filter_element in configuration.get("filter", [])]

    def __str__(self):
        return ''.join(
            [str(attribute) for attribute in self.__dict__.values()])
