#!/usr/bin/python3

import datetime
from signals.trading_signal import TradingSignalPoint


def calculate_third_point(p_0: TradingSignalPoint, p_1: TradingSignalPoint, date: datetime.datetime):
    nominator = p_1.value - p_0.value
    denumerator = p_1.date.timestamp() - p_0.date.timestamp()
    multiplier = date.timestamp() - p_0.date.timestamp()
    return (nominator / denumerator) * multiplier + p_0.value
