#!/usr/bin/python3

import time
import logging

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

    def send(self, message: mailing.message.Message) -> bool:
        msg = EmailMessage()
        msg['Subject'] = message.subject
        msg['From'] = self.configuration.sender
        msg['To'] = self.configuration.receiver
        msg.set_content(message.get())
        for i in range(10):
            try:
                self.server.login(self.configuration.sender,
                                  self.configuration.password)
                self.server.send_message(msg)
                self.server.quit()
                return True
            except (OSError, smtplib.SMTPException, smtplib.SMTPSenderRefused) as exc:
                logging.exception(exc)
                logging.warning("Could not send mail. Retrying after 10 secs.")
                time.sleep(10)
        return False
