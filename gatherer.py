#!/usr/bin/python3

import sys
import time
import logging
import traceback

import fetcher
import config.parser
import exchange.factory
import mailing.postman
import mailing.message
import storage.indicators
import storage.tickers
import storage.client


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

    markets = [
        parser.configuration.exchange.watched_market,
        parser.configuration.exchange.bearish_market,
        parser.configuration.exchange.bullish_market
    ]
    controller = exchange.factory.ExchangeControllerFactory.create(
        parser.configuration)

    fetchers = list()
    if isinstance(parser.configuration.market.candle_size, str):
        fetchers.append(
            fetcher.TradingViewFetcher(
                parser.configuration.market,
                parser.configuration.market.candle_size))
    elif isinstance(parser.configuration.market.candle_size, list):
        for candle_size in parser.configuration.market.candle_size:
            fetchers.append(
                fetcher.TradingViewFetcher(parser.configuration.market,
                                           candle_size))
    else:
        logging.critical("Invalid candle size parameter type.")
        return

    mailing.message.Message.bot_name = parser.configuration.mail.name
    postman = mailing.postman.Postman(parser.configuration.mail)
    postman.connect()

    client = storage.client.Client(parser.configuration.database.url,
                                   parser.configuration.database.user,
                                   parser.configuration.database.password)
    ticker_storage = storage.tickers.TickersStorage(client.database)
    indicator_storage = storage.indicators.IndicatorsStorage(client.database)

    try:
        while True:
            for market in markets:
                price = controller.get_price(market)
                ticker_storage.add(market.key, price)

            for tv_fetcher in fetchers:
                tv_fetcher.fetch_technical_indicator()
                indicator = tv_fetcher.get_technical_indicator()
                indicator_storage.add(tv_fetcher.market_name,
                                      tv_fetcher.candle_size, indicator)

            time.sleep(parser.configuration.market.check_interval)
    except KeyboardInterrupt:
        return
    except Exception as error:  # pylint: disable=broad-except
        message = mailing.error.ErrorMessage()
        message.compose(
            {"error": str(error) + "\n\n" + traceback.format_exc()})
        postman.send(message)
        logging.critical("Unhandled error occured %s.",
                         str(error) + "\n\n" + traceback.format_exc())


if __name__ == "__main__":
    main()
