#!/usr/bin/python3

import smtplib

import config.mail
import mailing.message


class Postman:
    def __init__(self, configuration: config.mail.MailConfig):
        self.configuration = configuration
        self.server = None

    def connect(self):
        self.server = smtplib.SMTP(self.configuration.smtp_server,
                                   self.configuration.port)
        self.server.login(self.configuration.sender,
                          self.configuration.password)

    def send(self, message: mailing.message.Message) -> bool:
        self.server.sendmail(self.configuration.sender,
                             self.configuration.receiver, message.get())
