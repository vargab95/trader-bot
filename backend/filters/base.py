#!/usr/bin/python3

import abc


class Filter:
    def __init__(self, length):
        self._length = length
        self._data = []
        self._value = None

    @abc.abstractmethod
    def put(self, value: float):
        pass  # pragma: no cover

    def get(self) -> float:
        return self._value

    @property
    def length(self):
        return self._length
