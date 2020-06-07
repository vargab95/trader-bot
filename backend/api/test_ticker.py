#!/usr/bin/python3

import unittest
from flask import Flask

from api.ticker import TickerOptions


class TickerOptionsTest(unittest.TestCase):
    def setUp(self):
        self.resource = TickerOptions()
        self.app = Flask("test")
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.payload = {'its': 'empty'}

    def test_get_response(self):
        pass
        # self.resource.get()
        # response = self.client.post('/ctrl', json=self.payload)
        # expected_resp = {'foo': 'bar'}
        # self.assertEqual(response.status_code, 200)
        # self.assertDictEqual(response.get_json(), expected_resp)
