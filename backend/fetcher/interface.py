#!/usr/bin/python3

import abc


class Fetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_technical_indicator(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_technical_indicator(self) -> float:
        pass  # pragma: no cover
