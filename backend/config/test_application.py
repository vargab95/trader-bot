#!/usr/bin/python3

import unittest

import config.application


class TestApplicationConfig(unittest.TestCase):
    @staticmethod
    def test_application_config():
        config.application.ApplicationConfig({})
