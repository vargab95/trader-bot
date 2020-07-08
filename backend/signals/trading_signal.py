#!/usr/bin/python3

import datetime
import typing
from dataclasses import dataclass


@dataclass
class TradingSignalPoint:
    value: float = 0.0
    date: datetime.datetime = None


@dataclass
class TradingSignalDescriptor:
    market: str = ""
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    limit: int = -1
    step: int = 1
    resolution: datetime.timedelta = None


@dataclass
class IndicatorSignalDescriptor(TradingSignalDescriptor):
    indicator: str = ""
    candle_size: str = ""


@dataclass
class TickerSignalDescriptor(TradingSignalDescriptor):
    pass


@dataclass
class TradingSignal:
    data: typing.List[TradingSignalPoint]
    descriptor: TradingSignalDescriptor
