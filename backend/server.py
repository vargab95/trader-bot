import sys
import logging
import traceback
from datetime import datetime

from flask import Flask
from flask_restful import reqparse, Api, Resource

import fetcher.base
import config.parser
import mailing.message
import mailing.postman
import storage.client
import storage.tickers
import storage.indicators

APP = Flask(__name__)
API = Api(APP)

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def convert_date_time(date_string):
    return datetime.strptime(date_string, DATE_TIME_FORMAT)


class Indicator(Resource):
    storage = None

    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('market', type=str, required=True)

        self.parser.add_argument(
            'indicator',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.indicator_name_map.keys()),
            required=True)

        self.parser.add_argument(
            'candle_size',
            type=str,
            choices=tuple(
                fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            required=True)

        self.parser.add_argument('start_date', type=convert_date_time)
        self.parser.add_argument('end_date', type=convert_date_time)
        self.parser.add_argument('limit', type=int, default=-1)

    def get(self):
        request = self.parser.parse_args()

        result = self.storage.get(request['market'], request['indicator'],
                                  request['candle_size'],
                                  request['start_date'], request['end_date'],
                                  request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(DATE_TIME_FORMAT)

        return result


class IndicatorOptions(Resource):
    def get(self):
        return {
            'market': ['GEMINI:BTCUSD'],
            'candle_size':
            list(fetcher.base.TradingViewFetcherBase.candle_size_map.keys()),
            'indicator':
            list(fetcher.base.TradingViewFetcherBase.indicator_name_map.keys())
        }


class Ticker(Resource):
    storage = None

    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('market', type=str, required=True)
        self.parser.add_argument('start_date', type=convert_date_time)
        self.parser.add_argument('end_date', type=convert_date_time)
        self.parser.add_argument('limit', type=int, default=-1)

    def get(self):
        request = self.parser.parse_args()

        result = self.storage.get(request['market'], request['start_date'],
                                  request['end_date'], request['limit'])

        for row in result:
            row['date'] = row['date'].strftime(DATE_TIME_FORMAT)

        return result


class TickerOptions(Resource):
    def get(self):
        return {'market': ['BTCUSDT']}


API.add_resource(Indicator, '/indicator')
API.add_resource(IndicatorOptions, '/indicator/options')
API.add_resource(Ticker, '/ticker')
API.add_resource(TickerOptions, '/ticker/options')


def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    parser = config.parser.ConfigurationParser()
    parser.read(sys.argv[1])
    logging.basicConfig(
        level=parser.configuration.logging.level,
        filename=parser.configuration.logging.path,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.debug(str(parser.configuration))

    mailing.message.Message.bot_name = parser.configuration.mail.name
    postman = mailing.postman.Postman(parser.configuration.mail)
    postman.connect()

    client = storage.client.Client(parser.configuration.database.url,
                                   parser.configuration.database.user,
                                   parser.configuration.database.password)
    Ticker.storage = storage.tickers.TickersStorage(client.database)
    Indicator.storage = storage.indicators.IndicatorsStorage(client.database)

    try:
        APP.run(debug=True)
    except KeyboardInterrupt:
        return
    except Exception as error:  # pylint: disable=broad-except
        message = mailing.error.ErrorMessage()
        message.compose(
            {"error": str(error) + "\n\n" + traceback.format_exc()})
        postman.send(message)
        logging.critical("Unhandled error occured %s.",
                         str(error) + "\n\n" + traceback.format_exc())


if __name__ == '__main__':
    main()