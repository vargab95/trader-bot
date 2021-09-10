#!/usr/bin/python3

import unittest

import config.application
import config.detector
import config.filter
import config.simulator
import config.parser
import config.common


class TestConfigParser(unittest.TestCase):
    def test_parse_fail(self):
        parser = config.parser.ConfigurationParser()
        with self.assertRaises(config.common.InvalidConfigurationException):
            parser.read("invalid")
