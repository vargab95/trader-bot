#!/usr/bin/python3

import typing

import mailing.message

MESSAGE = """
Dear user,

An unhandled error occured during the execution of the
TradingView bot. Please check the logs as soon as possible.

The error:
%s

Best regards:
The bot...
"""


class ErrorMessage(mailing.message.Message):
    def compose(self, data: typing.Dict) -> bool:
        self._message = MESSAGE % data["error"]
        self.subject = "{} - Error".format(self.bot_name)
