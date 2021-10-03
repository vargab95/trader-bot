import unittest

from config.database import DatabaseConfig
from config.common import InvalidConfigurationException


class TestDatabaseConfig(unittest.TestCase):
    def setUp(self):
        self.conf = DatabaseConfig({})
        self.conf.url = "test_url"
        self.conf.user = "test_user"
        self.conf.password = "test_password"
        self.conf.limit = 1

    def test_no_url_specified(self):
        self.conf.url = None
        self.conf.validate()

    def test_no_user_specified(self):
        self.conf.user = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_no_password_specified(self):
        self.conf.password = None
        with self.assertRaises(InvalidConfigurationException):
            self.conf.validate()

    def test_dict_generation(self):
        self.assertDictEqual(self.conf.dict(), {
            "url": "test_url",
            "user": "test_user",
            "password": "test_password",
            "limit": 1
        })
