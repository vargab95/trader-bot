#!/usr/bin/python3

import smtplib
from email.message import EmailMessage

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
        msg = EmailMessage()
        msg['Subject'] = message.subject
        msg['From'] = self.configuration.sender
        msg['To'] = self.configuration.receiver
        msg.set_content(message.get())
        self.server.send_message(msg)
