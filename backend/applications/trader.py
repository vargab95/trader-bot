#!/usr/bin/python

import logging

from datetime import datetime

import fetcher.single
import mailing.postman
import mailing.error
import mailing.statistics
import applications.base
import filters.sma
import trader.base
import trader.factory
import trader.common


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__long_term_fetcher: fetcher.base.TradingViewFetcherBase
        self.__filter: filters.base.Filter
        self.__trader: trader.base.TraderBase
        self.__last_sent_time: datetime

    def _initialize_application_logic(self):
        self._initialize_exchange()
        self._initialize_fetcher()

        if self._configuration.filter:
            self.__filter = filters.factory.FilterFactory.create_complex(
                self._configuration.filter)
        else:
            self.__filter = None

        self.__trader = trader.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()
        self.__last_sent_time = datetime.today()

    def _run_application_logic(self):
        while True:
            # TODO current_indicator = self.__get_indicator()
            current_indicator = self.__get_price()

            # TODO Initialize based on previous data
            if current_indicator:
                all_money = self.__get_all_money()
                self.__log_all_money(all_money)
                self.__trader.perform(current_indicator)
                self.__send_statistics_email(all_money)

            self._fetcher.sleep_until_next_data()

    # TODO Make it configurable which signal to use.
    # A new class should be created, for example, signal provider
    # which can provide both, trading view signals and signals for
    # exchanges.
    # For this purpose, the trading signals classes should be introduced
    # there too.
    def __get_indicator(self):
        indicator = self.__fetch_indicator()
        if self.__filter:
            return self.__apply_filter(indicator)
        return indicator

    def __get_price(self):
        ticker = self._exchange.get_price(
            self._configuration.exchange.watched_market)
        if self.__filter:
            return self.__apply_filter(ticker)
        return ticker

    def __fetch_indicator(self):
        self._fetcher.safe_fetch()
        return self._fetcher.get_technical_indicator()

    def __apply_filter(self, indicator):
        self.__filter.put(indicator)
        filtered = self.__filter.get()
        if filtered is None:
            logging.info("Waiting for filter to be filled.\n"
                         "    Input: %f\n"
                         "    Filtered: %s\n"
                         "    Length: %d",
                         indicator,
                         str(filtered),
                         self.__filter.length)
        return filtered

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
