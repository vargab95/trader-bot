#!/usr/bin/python3

import time
import logging
import traceback


def exchange_guard(timeout=5):
    def decorator(function):
        def wrapper(*args, **kwargs):
            for _ in range(10):
                try:
                    return function(*args, **kwargs)
                except Exception as exception:  # pylint: disable=broad-except
                    logging.error(
                        "Exception occured during exchange operation %s: %s",
                        function.__name__, str(exception))
                    logging.error(traceback.format_exc())
                    time.sleep(timeout)
            return False

        return wrapper

    return decorator
