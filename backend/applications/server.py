#!/usr/bin/python3

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import applications.base
import api.indicator
import api.ticker
import api.common

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class ServerApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__app: Flask
        self.__cors: CORS
        self.__api: Api

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()
        self.__initialize_flask_objects()
        self.__initialize_api_routes()
        api.common.DATE_TIME_FORMAT = \
            self._configuration.server.datetime_format
        api.ticker.Ticker.storage = self._ticker_storage
        api.indicator.Indicator.storage = self._indicator_storage

    def __initialize_flask_objects(self):
        self.__app = Flask(__name__)
        self.__cors = CORS(self.__app)
        self.__api = Api(self.__app)

    def __initialize_api_routes(self):
        api.indicator.Indicator.datetime_format = \
            self._configuration.server.datetime_format
        api.ticker.Ticker.datetime_format = \
            self._configuration.server.datetime_format

        self.__api.add_resource(api.indicator.Indicator, '/indicator')
        self.__api.add_resource(api.indicator.IndicatorOptions,
                                '/indicator/options')
        self.__api.add_resource(api.ticker.Ticker, '/ticker')
        self.__api.add_resource(api.ticker.TickerOptions, '/ticker/options')

    def _run_application_logic(self):
        if self._configuration.testing.enabled:
            self.__app.run(debug=True,
                           host='127.0.0.1',
                           port=self._configuration.server.port)
        else:
            self.__app.run(debug=False,
                           host='0.0.0.0',
                           port=self._configuration.server.port)
