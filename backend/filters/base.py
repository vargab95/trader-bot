#!/usr/bin/python3

import abc


class Filter:
    @abc.abstractmethod
    def put(self, value: float):
        pass

    @abc.abstractmethod
    def get(self) -> float:
        pass
