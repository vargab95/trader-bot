#!/usr/bin/python3

import datetime


class SignalBase:
    def __init__(self):
        self._id: int = 0
        self._name: str = ""
        self._start_date: datetime.datetime = None
        self._end_date: datetime.datetime = None
        self._color: str = ""
        self._step: int = 1
