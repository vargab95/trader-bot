#!/usr/bin/python3


class ConfigComponentBase:
    def validate(self):
        for attribute in self.__dict__.values():
            attribute.validate()

    def dict(self):
        result = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigComponentBase):
                result[key] = value.dict()
            else:
                result[key] = value
        return result
