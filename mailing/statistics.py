#!/usr/bin/python3

import typing

import mailing.message

MESSAGE = """
Dear user,

Your current money is %f.

Best regards:
The bot...
"""


class StatisticsMessage(mailing.message.Message):
    def compose(self, data: typing.Dict) -> bool:
        self._message = MESSAGE % data["all_money"]
