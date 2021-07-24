#!/usr/bin/python3

import copy


class ConfigComponentBase:
    def validate(self):
        for attribute in self.__dict__.values():
            attribute.validate()

    def dict(self):
        return copy.deepcopy(self.__dict__)
