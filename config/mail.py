#!/usr/bin/python3

import typing


class MailConfig:
    def __init__(self, config: typing.Dict):
        self.port = config.get("port", 465)
        self.smtp_server = config.get("server", "smtp.vbj.hu")
        self.sender = config.get("sender", "tvb@vbj.hu")
        self.receiver = config.get("receiver", None)
        self.password = config.get("password", None)

    def __str__(self):
        return "\nMail:" + \
               "\n    Port:     " + str(self.port) + \
               "\n    Server:   " + self.smtp_server + \
               "\n    Sender:   " + self.sender + \
               "\n    Receiver: " + self.receiver + \
               "\n    Password: " + str("*" * len(self.password))
