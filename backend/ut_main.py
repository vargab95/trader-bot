#!/usr/bin/python3

import unittest
import unittest.mock

import main


class MainTest(unittest.TestCase):
    def test_main_no_args(self):
        self.assertEqual(main.main(1, ["test"]), 1)

    def test_main_proper_args(self):
        with unittest.mock.patch('main.ApplicationFactory') as mock_factory:
            self.assertEqual(main.main(2, ["test", "trader"]), 0)
            mock_factory.create.assert_called_once()

    def test_main_improper_args(self):
        self.assertEqual(main.main(2, ["test", "non-existing application"]), 2)
