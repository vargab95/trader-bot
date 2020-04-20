#!/usr/bin/python3

import enum


class TradingAction(enum.Enum):
    HOLD = 0
    BUY_BULLISH = 1
    BUY_BEARISH = 2


class CurrentState(enum.Enum):
    NONE = 0
    BEAR = 1
    BULL = 2
