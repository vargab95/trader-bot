#!/usr/bin/python3

import enum

class TradingAction(enum.Enum):
    HOLD = 0
    SWITCH_TO_BULLISH = 1
    SWITCH_TO_BEARISH = 2
