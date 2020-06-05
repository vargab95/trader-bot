import unittest
import unittest.mock
import mailing.postman
import mailing.error
import mailing.statistics
import config.mail


class SMTPMock:

    def __init__(self, server: str, port: int, timeout: int = 0):
        self.server = server
        self.port = port
        self.timeout = timeout
        self.call_count = {
            "connect": 0,
            "ehlo": 0,
            "login": 0,
            "send_message": 0,
            "quit": 0
        }

    def connect(self, server: str, port: int):
        self.call_count["connect"] += 1

    def ehlo(self):
        self.call_count["ehlo"] += 1

    def login(self, sender: str, password: str):
        self.call_count["login"] += 1

    def send_message(self, msg):
        self.call_count["send_message"] += 1

    def quit(self):
        self.call_count["quit"] += 1


@unittest.mock.patch("smtplib.SMTP")
class MailingTest(unittest.TestCase):
    def setUp(self):
        self.postman = mailing.postman.Postman(config.mail.MailConfig({
            "name": "test",
            "password": "password",
            "receiver": "a@a.com",
        }))

    def test_send_statistics_message(self, smtp_mock):
        message = mailing.statistics.StatisticsMessage()
        message.compose({"all_money": 100})
        self.postman.send(message)

        smtp_mock.assert_called_once()
        handle = smtp_mock()
        handle.connect.assert_called_once()
        handle.ehlo.assert_called_once()
        handle.login.assert_called_once()
        handle.send_message.assert_called_once()
        handle.quit.assert_called_once()

    def test_send_error_message(self, smtp_mock):
        message = mailing.error.ErrorMessage()
        message.compose({"error": "Error"})
        self.postman.send(message)

        smtp_mock.assert_called_once()
        handle = smtp_mock()
        handle.connect.assert_called_once()
        handle.ehlo.assert_called_once()
        handle.login.assert_called_once()
        handle.send_message.assert_called_once()
        handle.quit.assert_called_once()
