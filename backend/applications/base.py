#!/usr/bin/python

import sys
import logging
import traceback
import abc

import config.parser
import config.logging
import exchange.interface
import exchange.factory
import mailing.postman
import mailing.error
import storage.client
import storage.tickers
import storage.indicators
import fetcher.single
import fetcher.multi
import fetcher.base


class ApplicationInitializationException(Exception):
    pass


class ApplicationBase:
    def __init__(self):
        self._configuration: config.application.ApplicationConfig
        self._configuration_file_path: str
        self._postman: mailing.postman.Postman
        self._client: storage.client.Client
        self._ticker_storage: storage.tickers.TickersStorage
        self._indicator_storage: storage.indicators.IndicatorsStorage
        self._exchange: exchange.interface.ExchangeInterface
        self._fetcher: fetcher.base.TradingViewFetcherBase

    def _initialize_storages(self):
        self._initialize_ticker_storage()
        self._initialize_indicator_storage()

    def _initialize_client(self):
        self._client = storage.client.Client(
            self._configuration.database.url,
            self._configuration.database.user,
            self._configuration.database.password)

    def _initialize_ticker_storage(self):
        self._ticker_storage = storage.tickers.TickersStorage(
            self._client.database)

    def _initialize_indicator_storage(self):
        self._indicator_storage = storage.indicators.IndicatorsStorage(
            self._client.database)

    def _initialize_fetcher(self):
        if isinstance(self._configuration.trader.candle_size, str):
            self._fetcher = fetcher.single.TradingViewFetcherSingle(
                self._configuration.trader)
        elif isinstance(self._configuration.trader.candle_size, list):
            self._fetcher = fetcher.multi.TradingViewFetcherMulti(
                self._configuration.trader)
        else:
            logging.critical("Invalid candle size parameter type.")
            raise ApplicationInitializationException()

    def _initialize_exchange(self):
        self._exchange = exchange.factory.ExchangeControllerFactory.create(
            self._configuration)

    def initialize(self):
        self._process_command_line_arguments()
        self._parse_configuration()
        self._set_class_variables()
        self._configure_logging()
        self._initialize_mailing()
        self._initialize_application_logic()
        logging.debug(str(self._configuration))

    def _process_command_line_arguments(self):
        if len(sys.argv) != 3:
            print("Usage:", sys.argv[0], "<application>",
                  "<configuration file>")
            sys.exit(1)
        self._configuration_file_path = sys.argv[2]

    def _parse_configuration(self):
        parser = config.parser.ConfigurationParser()
        parser.read(self._configuration_file_path)
        self._configuration = parser.configuration

    def _configure_logging(self):
        logging.basicConfig(
            level=self._configuration.logging.level,
            filename=self._configuration.logging.path,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _set_class_variables(self):
        exchange.interface.Market.name_format = \
            self._configuration.exchange.market_name_format
        mailing.message.Message.bot_name = self._configuration.mail.name

    def _initialize_mailing(self):
        self._postman = mailing.postman.Postman(self._configuration.mail)

    @abc.abstractmethod
    def _initialize_application_logic(self):
        pass

    @abc.abstractmethod
    def _run_application_logic(self):
        pass

    def run(self):
        try:
            self._run_application_logic()
        except KeyboardInterrupt:
            return
        except Exception as error:  # pylint: disable=broad-except
            message = mailing.error.ErrorMessage()
            message.compose(
                {"error": str(error) + "\n\n" + traceback.format_exc()})
            self._postman.send(message)
            logging.critical("Unhandled error occured %s.",
                             str(error) + "\n\n" + traceback.format_exc())
