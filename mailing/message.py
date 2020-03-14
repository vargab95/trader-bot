#!/usr/bin/python3

import abc
import typing


class InvalidMessageException(Exception):
    pass


class Message(metaclass=abc.ABCMeta):
    def __init__(self):
        self._message = None
        self.subject = ""

    @abc.abstractmethod
    def compose(self, data: typing.Dict) -> bool:
        pass

    def get(self) -> str:
        if not self._message:
            raise InvalidMessageException()
        return self._message

    def reset(self):
        self._message = None
