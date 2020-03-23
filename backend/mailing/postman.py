#!/usr/bin/python3

import time
import logging
import socket

import smtplib
from email.message import EmailMessage

import config.mail
import mailing.message


class Postman:
    def __init__(self, configuration: config.mail.MailConfig):
        self.configuration = configuration
        self.server = None
        self.connected = False

    def connect(self):
        for _ in range(3):
            try:
                logging.debug("Connecting to mail server")
                self.server = smtplib.SMTP(self.configuration.smtp_server,
                                           self.configuration.port,
                                           timeout=5)
                self.connected = True
                logging.info("Postman was initialized")
                break
            except (TimeoutError, ConnectionRefusedError, socket.timeout):
                logging.error("Cannot connect to the mail server.")
                time.sleep(5)

    def send(self, message: mailing.message.Message) -> bool:
        if not self.connected:
            return False

        msg = EmailMessage()
        msg['Subject'] = message.subject
        msg['From'] = self.configuration.sender
        msg['To'] = self.configuration.receiver
        msg.set_content(message.get())
        for _ in range(10):
            try:
                self.server.login(self.configuration.sender,
                                  self.configuration.password)
                self.server.send_message(msg)
                self.server.quit()
                return True
            except (OSError, smtplib.SMTPException,
                    smtplib.SMTPSenderRefused) as exc:
                logging.exception(exc)
                logging.warning("Could not send mail. Retrying after 10 secs.")
                time.sleep(10)
        return False
