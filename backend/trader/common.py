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


BULLISH_STATES = [TraderState.BULLISH,
                  TraderState.SELLING_BULLISH,
                  TraderState.BUYING_BULLISH]
BEARISH_STATES = [TraderState.BEARISH,
                  TraderState.SELLING_BEARISH,
                  TraderState.BUYING_BEARISH]
