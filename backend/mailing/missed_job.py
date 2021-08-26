#!/usr/bin/python3

import typing

import mailing.message

MESSAGE = """
Dear user,

The job %s could not be executed in the bot.
Please check the logs as soon as possible.

Best regards:
The bot...
"""


class MissedJobMessage(mailing.message.Message):
    def compose(self, data: typing.Dict) -> bool:
        self._message = MESSAGE % data["job_name"]
        self.subject = "{} - Missed execution".format(self.bot_name)
        return True
