#!/usr/bin/python

import logging

from datetime import datetime

import fetcher.single
import mailing.postman
import mailing.error
import mailing.statistics
import applications.base
import filters.sma
import traders.base
import traders.factory
import traders.common


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__long_term_fetcher: fetcher.base.TradingViewFetcherBase
        self.__sma: filters.sma.SMA
        self.__trader: traders.base.TraderBase
        self.__last_sent_time: datetime

    def _initialize_application_logic(self):
        self._initialize_exchange()
        self._initialize_fetcher()

        if self._configuration.market.indicator_sma > 1:
            self.__sma = filters.sma.SMA(
                self._configuration.market.indicator_sma)
        else:
            self.__sma = None

        self.__trader = traders.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()
        self.__last_sent_time = datetime.today()

    def _run_application_logic(self):
        while True:
            current_indicator = self.__get_indicator()

            if current_indicator:
                all_money = self.__get_all_money()
                self.__log_all_money(all_money)
                self.__trader.perform(current_indicator)
                self.__send_statistics_email(all_money)

            self._fetcher.sleep_until_next_data()

    def __get_indicator(self):
        indicator = self.__fetch_indicator()
        if self.__sma:
            return self.__apply_sma(indicator)
        return indicator

    def __fetch_indicator(self):
        self._fetcher.safe_fetch()
        return self._fetcher.get_technical_indicator()

    def __apply_sma(self, indicator):
        self.__sma.put(indicator)
        sma = self.__sma.get()
        if not sma:
            logging.info(
                "Waiting for SMA to be filled. "
                "Current length: %d "
                "Final length: %d ", self.__sma.length,
                self._configuration.market.indicator_sma)
        return self.__sma.get()

    def __log_all_money(self, all_money):
        logging.info("All money: %f", all_money)
        logging.debug(self._exchange.get_balances())

    def __get_all_money(self):
        return self._exchange.get_money(
            self._configuration.exchange.watched_market.base)

    def __send_statistics_email(self, all_money):
        current_time = datetime.today()
        if current_time > self.__last_sent_time:
            self.__last_sent_time = current_time.replace(day=current_time.day +
                                                         1,
                                                         hour=1,
                                                         minute=0,
                                                         second=0,
                                                         microsecond=0)

            message = mailing.statistics.StatisticsMessage()
            message.compose({"all_money": all_money})
            self._postman.send(message)