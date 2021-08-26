#!/usr/bin/python3

import typing
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
        self.__mailing_queue: typing.List[mailing.message.Message] = list()

    def connect(self):
        if not self.__configuration.enabled:
            return True

        try:
            logging.debug("Connecting to mail server")
            self.__server = smtplib.SMTP(self.__configuration.smtp_server,
                                         self.__configuration.port,
                                         timeout=5)
            self.__server.connect(self.__configuration.smtp_server,
                                  self.__configuration.port)

            self.__server.ehlo()
            self.__server.starttls()
            self.__server.ehlo()

            self.__server.login(self.__configuration.sender,
                                self.__configuration.password)
            return True
        except (TimeoutError, ConnectionRefusedError, socket.timeout) as exc:
            logging.exception(exc)
            logging.error("Cannot connect to the mail server.")

        return False

    def add_message_to_queue(self, message: mailing.message.Message) -> bool:
        if self.__configuration.enabled:
            self.__mailing_queue.append(message)

    def send_all(self):
        while self.__mailing_queue:
            if self.send(self.__mailing_queue[0]):
                self.__mailing_queue.pop(0)

    def send(self, message: mailing.message.Message) -> bool:
        if not self.__configuration.enabled:
            return True

        msg = EmailMessage()
        msg['Subject'] = message.subject
        msg['From'] = self.__configuration.sender
        msg['To'] = self.__configuration.receiver
        msg.set_content(message.get())
        try:
            if not self.connect():
                return False
            self.__server.send_message(msg)
            self.__server.quit()
            return True
        except (OSError, smtplib.SMTPException, smtplib.SMTPSenderRefused) as exc:
            logging.exception(exc)
        return False
