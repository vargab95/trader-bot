#!/usr/bin/python3

import enum


class BuyState(enum.Enum):
    NONE = 1
    BULLISH = 2
    BEARISH = 3
    SWITCHING_TO_BULLISH = 4
    SWITCHING_TO_BEARISH = 5
