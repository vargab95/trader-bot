#!/usr/bin/python3

import enum


class TraderState(enum.Enum):
    BASE = 1
    BUYING_BULLISH = 2
    BUYING_BEARISH = 3
    SELLING_BULLISH = 4
    SELLING_BEARISH = 5
    BULLISH = 6
    BEARISH = 7
