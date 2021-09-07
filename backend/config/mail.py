#!/usr/bin/python3

import typing

from config.base import ConfigComponentBase
from config.common import InvalidConfigurationException


class MailConfig(ConfigComponentBase):
    def __init__(self, config: typing.Dict):
        self.enabled = config.get("enabled", False)
        self.name = config.get("name", "TradingViewBot")
        self.port = config.get("port", 25)
        self.smtp_server = config.get("smtp_server", None)
        self.sender = config.get("sender", None)
        self.receiver = config.get("receiver", None)
        self.password = config.get("password", None)

    def validate(self):
        if self.enabled:
            if self.smtp_server is None:
                raise InvalidConfigurationException("SMTP server is a mandatory parameter for mailing")

            if self.sender is None:
                raise InvalidConfigurationException("Sender is a mandatory parameter for mailing")

            if self.receiver is None:
                raise InvalidConfigurationException("Receiver is a mandatory parameter for mailing")

            if self.password is None:
                raise InvalidConfigurationException("Password is a mandatory parameter for mailing")

    def dict(self):
        result = super().dict()
        result["password"] = "*" * 10
        return result
