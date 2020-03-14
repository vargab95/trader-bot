#!/usr/bin/python3

import logging

import binance.exceptions


def exchange_guard(function):
    def decorator(*args, **kwargs):
        for _ in range(30):
            try:
                return function(*args, **kwargs)
            except binance.exceptions.BinanceAPIException as api_exception:
                logging.error(
                    "Exception occured during exchange operation %s: %s",
                    function.__name__, str(api_exception))
        return False

    return decorator
