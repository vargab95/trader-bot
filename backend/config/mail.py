#!/usr/bin/python3

import typing


class MailConfig:
    def __init__(self, config: typing.Dict):
        self.name = config.get("name", "TradingViewBot")
        self.port = config.get("port", 25)
        self.smtp_server = config.get("smtp_server", "smtp.vbj.hu")
        self.sender = config.get("sender", "tvb@vbj.hu")
        self.receiver = config.get("receiver", "")
        self.password = config.get("password", "")

    def __str__(self):
        return "\nMail:" + \
               "\n    Name:     " + self.name + \
               "\n    Port:     " + str(self.port) + \
               "\n    Server:   " + self.smtp_server + \
               "\n    Sender:   " + self.sender + \
               "\n    Receiver: " + str(self.receiver) + \
               "\n    Password: " + str("*" * len(self.password))
