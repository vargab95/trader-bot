#!/usr/bin/python3

import time
import logging
import json

import binance.exceptions
import requests.exceptions


def exchange_guard(function):
    def decorator(*args, **kwargs):
        for _ in range(1000):
            try:
                return function(*args, **kwargs)
            except Exception as exception:
                logging.error(
                    "Exception occured during exchange operation %s: %s",
                    function.__name__, str(exception))
                time.sleep(5)
        return False

    return decorator
