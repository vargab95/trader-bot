#!/usr/bin/python

import logging
import enum

from datetime import datetime

import fetcher.single
import detector.factory
import detector.common
import mailing.postman
import mailing.error
import mailing.statistics
import applications.base


class BuyState(enum.Enum):
    NONE = 1
    BULLISH = 2
    BEARISH = 3
    SWITCHING_TO_BULLISH = 4
    SWITCHING_TO_BEARISH = 5


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__(self)
        self.__long_term_fetcher: fetcher.base.TradingViewFetcherBase
        self.__detector: detector.interface.DetectorInterface

    def _initialize_application_logic(self):
        self._initialize_exchange()
        self._initialize_fetcher()
        if self._configuration.market.follower_enabled:
            self.__long_term_fetcher = self.__initialize_long_term_fetcher()
            self.__initialize_detector(self.__long_term_fetcher)

    def __initialize_long_term_fetcher(self):
        return fetcher.single.TradingViewFetcherSingle(
            self._configuration.market,
            self._configuration.market.follower_candle_size)

    def __initialize_detector(self, long_term_fetcher):
        self.__detector = detector.factory.DetectorFactory.create(
            self._configuration.market, long_term_fetcher)

    def _run_application_logic(self):
        self._fetcher.safe_fetch()
        current_indicator = 0.0
        state = BuyState.NONE
        sma = list()
        next_time = datetime.today()
        while True:
            self._fetcher.safe_fetch()
            current_indicator = self._fetcher.get_technical_indicator()
            sma.append(current_indicator)

            if len(sma) <= self._configuration.market.indicator_sma:
                logging.info(
                    "Waiting for SMA to be filled. "
                    "Current length: %d "
                    "Final length: %d ", len(sma),
                    self._configuration.market.indicator_sma)
            else:
                sma.pop(0)
                current_indicator = sum(
                    sma) / self._configuration.market.indicator_sma
                action = self.__detector.check(current_indicator)

                logging.debug("Detector has returned %s", str(action))
                logging.debug("Current state is %s", str(state))

                if action == detector.common.TradingAction.SWITCH_TO_BULLISH:
                    if state != BuyState.BULLISH:
                        state = BuyState.SWITCHING_TO_BULLISH
                elif action == detector.common.TradingAction.SWITCH_TO_BEARISH:
                    if state != BuyState.BEARISH:
                        state = BuyState.SWITCHING_TO_BEARISH

                logging.debug("New state is %s", str(state))

                state = BuyState.SWITCHING_TO_BULLISH
                if state == BuyState.SWITCHING_TO_BULLISH:
                    available_amount = self._exchange.get_balance(
                        self._configuration.exchange.bearish_market.target)
                    if available_amount > 0.0:
                        self._exchange.sell(
                            self._configuration.exchange.bearish_market,
                            available_amount)
                    else:
                        logging.warning(
                            "Cannot sell bear due to insufficient amount")

                    balance = self._exchange.get_balance(
                        self._configuration.exchange.bullish_market.base)
                    price = self._exchange.get_price(
                        self._configuration.exchange.bullish_market)
                    amount_to_buy = balance / price
                    if amount_to_buy > 0.0:
                        if self._exchange.buy(
                                self._configuration.exchange.bullish_market,
                                amount_to_buy):
                            state = BuyState.BULLISH
                    else:
                        logging.warning(
                            "Cannot buy bull due to insufficient money")

                    logging.info("New balance: %s",
                                 str(self._exchange.get_balances()))
                elif state == BuyState.SWITCHING_TO_BEARISH:
                    available_amount = self._exchange.get_balance(
                        self._configuration.exchange.bullish_market.target)
                    if available_amount > 0.0:
                        self._exchange.sell(
                            self._configuration.exchange.bullish_market,
                            available_amount)
                    else:
                        logging.warning(
                            "Cannot sell bull due to insufficient amount")

                    balance = self._exchange.get_balance(
                        self._configuration.exchange.bearish_market.base)
                    price = self._exchange.get_price(
                        self._configuration.exchange.bearish_market)
                    amount_to_buy = balance / price
                    if amount_to_buy > 0.0:
                        if self._exchange.buy(
                                self._configuration.exchange.bearish_market,
                                amount_to_buy):
                            state = BuyState.BEARISH
                    else:
                        logging.warning(
                            "Cannot buy bear due to insufficient money")

                    logging.info("New balance: %s",
                                 str(self._exchange.get_balances()))
                logging.info(
                    "Current price: %f",
                    self._exchange.get_price(
                        self._configuration.exchange.watched_market))
                all_money = self._exchange.get_money("USD")
                logging.info("All money: %f", all_money)
                logging.debug(self._exchange.get_balances())

                current_time = datetime.today()
                if current_time > next_time:
                    next_time = current_time.replace(day=current_time.day + 1,
                                                     hour=1,
                                                     minute=0,
                                                     second=0,
                                                     microsecond=0)

                    message = mailing.statistics.StatisticsMessage()
                    message.compose({"all_money": all_money})
                    self._postman.send(message)

            self._fetcher.sleep_until_next_data()
