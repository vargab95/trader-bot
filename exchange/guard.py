#!/usr/bin/python3

import time
import logging
import json

import binance.exceptions
import requests.exceptions

def exchange_guard(function):
    def decorator(*args, **kwargs):
        for _ in range(30):
            try:
                return function(*args, **kwargs)
            except (requests.exceptions.ConnectionError, binance.exceptions.BinanceAPIException) as api_exception:
                logging.error(
                    "Exception occured during exchange operation %s: %s",
                    function.__name__, str(api_exception))
                time.sleep(5)
        return False

    return decorator
