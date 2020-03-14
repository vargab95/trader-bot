#!/usr/bin/python3

import abc
import typing


class InvalidMessageException(Exception):
    pass


class Message(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__message = None

    @abc.abstractmethod
    def compose(self, data: typing.Dict) -> bool:
        pass

    def get(self) -> str:
        if not self.__message:
            raise InvalidMessageException()
        return self.__message

    def reset(self):
        self.__message = None
