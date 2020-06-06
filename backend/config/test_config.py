#!/usr/bin/python3

import unittest

import config.application
import config.detector
import config.filter
import config.simulator
import config.parser
import config.common


class ConfigTest(unittest.TestCase):
    # This test is only for checking typos
    def test_run_on_all_lines(self):
        self.assertNotEqual(str(config.application.ApplicationConfig({})), "")

    def test_run_simulator_on_all_lines(self):
        self.assertNotEqual(str(config.simulator.SimulatorConfig({})), "")

    def test_run_detector_on_all_lines(self):
        self.assertNotEqual(str(config.detector.DetectorConfig({})), "")

    def test_run_filter_on_all_lines(self):
        self.assertNotEqual(str(config.filter.FilterConfig({})), "")

    def test_parse(self):
        parser = config.parser.ConfigurationParser()
        parser.read("conf.yml")
        self.assertIsInstance(parser.configuration,
                              config.application.ApplicationConfig)

    def test_parse_fail(self):
        parser = config.parser.ConfigurationParser()
        try:
            parser.read("invalid")
            self.fail()
        except config.common.InvalidConfigurationException:
            pass
