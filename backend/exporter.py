#!/usr/bin/python3

import sys
import logging
import json

import config.parser
import storage.client
import storage.indicators
import storage.tickers
import utils.estimators


def main():
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "<configuration file>", "<output file>")
        sys.exit(1)

    parser = config.parser.ConfigurationParser()
    parser.read(sys.argv[1])
    logging.basicConfig(
        level=parser.configuration.logging.level,
        filename=parser.configuration.logging.path,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.debug(str(parser.configuration))

    client = storage.client.Client(parser.configuration.database.url,
                                   parser.configuration.database.user,
                                   parser.configuration.database.password)
    ticker_storage = storage.tickers.TickersStorage(client.database)
    indicator_storage = storage.indicators.IndicatorsStorage(client.database)

    watched_market_data = ticker_storage.get(
        market=parser.configuration.exchange.watched_market.key,
        limit=parser.configuration.database.limit)
    bearish_market_data = ticker_storage.get(
        market=parser.configuration.exchange.bearish_market.key,
        limit=parser.configuration.database.limit)
    bullish_market_data = ticker_storage.get(
        market=parser.configuration.exchange.bullish_market.key,
        limit=parser.configuration.database.limit)
    indicator_data = indicator_storage.get(
        market=parser.configuration.market.name,
        indicator="all",
        candle_size=parser.configuration.market.candle_size,
        limit=parser.configuration.database.limit)

    result = []
    for line in watched_market_data:
        result.append({
            "date":
            line["date"].isoformat(),
            "watched":
            line["price"],
            "bearish":
            utils.estimators.get_linear_estimation(bearish_market_data,
                                                   line["date"]),
            "bullish":
            utils.estimators.get_linear_estimation(bullish_market_data,
                                                   line["date"]),
            "indicator":
            utils.estimators.get_linear_estimation(indicator_data,
                                                   line["date"])
        })

    with open(sys.argv[2], "w") as output_file:
        json.dump(result, output_file, indent=4)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
