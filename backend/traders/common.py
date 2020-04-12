#!/usr/bin/python3

import enum
import typing

import exchange.interface


class ActionType(enum.Enum):
    BUY = 1
    SELL = 2


class TradingAction:
    def __init__(self,
                 action_type: ActionType,
                 market: exchange.interface.Market,
                 amount: float = 0.0):
        self.market = market
        self.type = action_type
        self.amount = amount


class TradingActions:
    def __init__(self):
        self.__actions: typing.Dict[ActionType,
                                    typing.List[TradingAction]] = dict()

    def add_action(self, action: TradingAction):
        self.__actions[action.type].append(action)

    def get_buy_actions(self) -> TradingAction:
        for action in self.__actions[ActionType.BUY]:
            yield action

    def get_sell_actions(self) -> TradingAction:
        for action in self.__actions[ActionType.SELL]:
            yield action


class BuyState(enum.Enum):
    NONE = 1
    BULLISH = 2
    BEARISH = 3
    SWITCHING_TO_BULLISH = 4
    SWITCHING_TO_BEARISH = 5
