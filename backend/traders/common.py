#!/usr/bin/python3

import enum


class BuyState(enum.Enum):
    NONE = 1
    BUYING_BULLISH = 2
    BUYING_BEARISH = 3
    BULLISH_BOUGHT = 4
    BEARISH_BOUGHT = 5


class SellState(enum.Enum):
    NONE = 1
    SELLING_BULLISH = 2
    SELLING_BEARISH = 3
    BULLISH_SOLD = 4
    BEARISH_SOLD = 5


class TraderState(enum.Enum):
    BASE = 1
    BUYING_BULLISH = 2
    BUYING_BEARISH = 3
    SELLING_BULLISH = 4
    SELLING_BEARISH = 5
    BULLISH = 6
    BEARISH = 7
