#!/usr/bin/python

import sys
import logging
import traceback
import abc

import config.parser
import config.logging
import mailing.postman
import mailing.error
import storage.client
import storage.tickers
import storage.indicators
from builder.base import TradingComponentsBuilderBase


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
        self._builder: TradingComponentsBuilderBase = TradingComponentsBuilderBase()

    def _initialize_storages(self):
        self._initialize_ticker_storage()
        self._initialize_indicator_storage()

    def _initialize_client(self):
        self._client = storage.client.Client(self._configuration.database.url,
                                             self._configuration.database.user,
                                             self._configuration.database.password)

    def _initialize_ticker_storage(self):
        self._ticker_storage = storage.tickers.TickersStorage(self._client.database)

    def _initialize_indicator_storage(self):
        self._indicator_storage = storage.indicators.IndicatorsStorage(self._client.database)

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
            print("Usage:", sys.argv[0], "<application>", "<configuration file>")
            sys.exit(1)
        self._configuration_file_path = sys.argv[2]

    def _parse_configuration(self):
        parser = config.parser.ConfigurationParser()
        parser.read(self._configuration_file_path)
        self._configuration = parser.configuration
        self._configuration.validate()

    def _set_class_variables(self):
        mailing.message.Message.bot_name = self._configuration.mail.name

    def _configure_logging(self):
        if self._configuration.logging.path:
            logging.basicConfig(level=self._configuration.logging.level,
                                filename=self._configuration.logging.path,
                                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        else:
            logging.basicConfig(level=self._configuration.logging.level,
                                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _initialize_mailing(self):
        self._postman = mailing.postman.Postman(self._configuration.mail)

    @abc.abstractmethod
    def _initialize_application_logic(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _run_application_logic(self):  # pragma: no cover
        pass

    def run(self):
        try:
            self._run_application_logic()
        except KeyboardInterrupt:
            logging.info("Process was stopped by keyboard interrupt")
            return
        except Exception as error:  # pylint: disable=broad-except
            message = mailing.error.ErrorMessage()
            message.compose({"error": str(error) + "\n\n" + traceback.format_exc()})
            self._postman.send(message)
            logging.critical("Unhandled error occured %s.", str(error) + "\n\n" + traceback.format_exc())
            raise error
