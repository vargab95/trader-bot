#!/usr/bin/python3

import enum


class TradingAction(enum.Enum):
    HOLD_SIGNAL = 0
    BULLISH_SIGNAL = 1
    BEARISH_SIGNAL = 2
    RETURN_TO_BASE_SIGNAL = 3


class CurrentState(enum.Enum):
    NONE = 0
    BEAR = 1
    BULL = 2
