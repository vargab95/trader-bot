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
        self.__configuration = configuration
        self.__server = None

    def connect(self):
        for _ in range(3):
            try:
                logging.debug("Connecting to mail server")
                self.__server = smtplib.SMTP(self.__configuration.smtp_server,
                                             self.__configuration.port,
                                             timeout=5)
                self.__server.connect(self.__configuration.smtp_server,
                                      self.__configuration.port)
                self.__server.ehlo()
                self.__server.login(self.__configuration.sender,
                                    self.__configuration.password)
                return True
            except (TimeoutError, ConnectionRefusedError, socket.timeout):
                logging.error("Cannot connect to the mail server.")
                time.sleep(5)
        return False

    def send(self, message: mailing.message.Message) -> bool:
        msg = EmailMessage()
        msg['Subject'] = message.subject
        msg['From'] = self.__configuration.sender
        msg['To'] = self.__configuration.receiver
        msg.set_content(message.get())
        for _ in range(10):
            try:
                if not self.connect():
                    return False
                self.__server.send_message(msg)
                self.__server.quit()
                return True
            except (OSError, smtplib.SMTPException,
                    smtplib.SMTPSenderRefused) as exc:
                logging.exception(exc)
                logging.warning("Could not send mail. Retrying after 10 secs.")
                time.sleep(10)
        return False
