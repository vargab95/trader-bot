#!/usr/bin/python3

import unittest

import config.mail
import mailing.postman
import mailing.message
import mailing.error
import mailing.statistics


class MailingTest(unittest.TestCase):
    def setUp(self):
        self.configuration = config.mail.MailConfig({
            "receiver": "",
            "password": ""
        })
        self.postman = mailing.postman.Postman(self.configuration)
        self.postman.connect()

    def test_send_error(self):
        message = mailing.error.ErrorMessage()
        message.compose({"error": "Test error"})
        self.postman.send(message)

    def test_send_statistics(self):
        message = mailing.statistics.StatisticsMessage()
        message.compose({"all_money": 100.0})
        self.postman.send(message)
