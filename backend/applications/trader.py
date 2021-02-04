#!/usr/bin/python

import logging

from datetime import datetime
from datetime import timedelta

import fetcher.single
import mailing.postman
import mailing.error
import mailing.statistics
import applications.base
import filters.sma
import trader.base
import trader.factory
import trader.common
from trader.common import TraderState
import signals.trading_signal


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__long_term_fetcher: fetcher.base.TradingViewFetcherBase
        self.__filter: filters.base.Filter
        self.__trader: trader.base.TraderBase
        self.__last_sent_time: datetime
        self.__first_mail_sent: bool = False

    def _initialize_application_logic(self):
        self._initialize_exchange()
        self._initialize_fetcher()

        self.__initialize_real_time()
        if self._configuration.trader.filters:
            self.__filter = filters.factory.FilterFactory.create_complex(
                self._configuration.trader.filters)
            for point in self._configuration.trader.initial_values:
                self.__filter.put(point.value)
        else:
            self.__filter = None

        self.__trader = trader.factory.TraderFactory.create(
            self._configuration, self._exchange)
        self.__trader.initialize()
        self.__last_sent_time = datetime.today()

    __candle_size_resolution_map = {
        "1m": timedelta(seconds=60),
        "5m": timedelta(seconds=60 * 5),
        "15m": timedelta(seconds=60 * 15),
        "1h": timedelta(seconds=3600),
        "4h": timedelta(seconds=3600 * 4),
        "1D": timedelta(seconds=3600 * 24),
        "1W": timedelta(seconds=3600 * 24 * 7),
        "1M": timedelta(seconds=3600 * 24 * 30)
    }

    def __initialize_real_time(self):
        if self._configuration.trader.initial_values == []:
            resolution = self.__candle_size_resolution_map[self._configuration.trader.candle_size]
            logging.debug("Initialize real time: resolution: %d, initial_length: %d, initial_step: %d",
                          resolution, self._configuration.trader.initial_length, self._configuration.trader.initial_step)
            descriptor = signals.trading_signal.TickerSignalDescriptor(
                market=self._configuration.exchange.watched_market,
                limit=self._configuration.trader.initial_length * self._configuration.trader.initial_step,
                resolution=resolution,
                start_date=datetime.now() - resolution * \
                                            self._configuration.trader.initial_length * \
                                            self._configuration.trader.initial_step)
            self._configuration.trader.initial_values = self._exchange.get_price_history(
                descriptor,
                self._configuration.trader.initial_keyword).data[::self._configuration.trader.initial_step]
            logging.debug("Fetched elements: %s", str(self._configuration.trader.initial_values))

    def _run_application_logic(self):
        while True:
            # TODO current_indicator = self.__get_indicator()
            current_indicator = self.__get_price()
            # FIXME Check whether an exchange do not have the pair
            # to calculate all_money
            # all_money = self.__get_all_money()

            if current_indicator is not None:
                logging.info("Indicator: %f", current_indicator)
                # logging.info("All money: %f", all_money)
                logging.info("State: %s", self.__trader.state)
                logging.info(self._exchange.get_balances())
                self.__trader.perform(current_indicator)

            # self.__send_statistics_email(all_money)
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
        used_keyword = self._configuration.exchange.default_price_keyword

        if self.__trader.state in [TraderState.BULLISH, TraderState.BUYING_BULLISH]:
            used_keyword = self._configuration.exchange.bullish_price_keyword

        if self.__trader.state in [TraderState.BEARISH, TraderState.BUYING_BEARISH]:
            used_keyword = self._configuration.exchange.bearish_price_keyword

        ticker = self._exchange.get_price(
            self._configuration.exchange.watched_market, keyword=used_keyword)
        logging.debug("Unfiltered price of %s: %f",
                      self._configuration.exchange.watched_market.key, ticker)
        if self.__filter:
            return self.__apply_filter(ticker)
        return ticker

    def __fetch_indicator(self):
        self._fetcher.safe_fetch()
        return self._fetcher.get_technical_indicator()

    def __apply_filter(self, indicator):
        self.__filter.put(indicator)
        filtered = self.__filter.get()
        logging.debug("Filtered price of %s: %s",
                      self._configuration.exchange.watched_market.key, str(filtered))
        if filtered is None:
            logging.info("Waiting for filter to be filled.\n"
                         "    Input: %f\n"
                         "    Filtered: %s\n"
                         "    Length: %d",
                         indicator,
                         str(filtered),
                         self.__filter.length)
        return filtered

    def __get_all_money(self):
        return self._exchange.get_money(
            self._configuration.exchange.watched_market.base)

    def __send_statistics_email(self, all_money):
        current_time = datetime.today()
        if (not self.__first_mail_sent) or (current_time > (self.__last_sent_time + timedelta(days=1))):
            logging.debug("Mail period exceeded or first mail is to sent out")
            self.__first_mail_sent = True
            self.__last_sent_time = current_time
            message = mailing.statistics.StatisticsMessage()
            message.compose({"all_money": all_money})
            self._postman.send(message)
