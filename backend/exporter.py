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

    watched_market_data = sorted(watched_market_data,
                                 key=lambda item: item["date"])
    bearish_market_data = sorted(bearish_market_data,
                                 key=lambda item: item["date"])
    bullish_market_data = sorted(bullish_market_data,
                                 key=lambda item: item["date"])
    indicator_data = sorted(indicator_data, key=lambda item: item["date"])

    bearish_idx = 0
    bullish_idx = 0
    indicator_idx = 0

    result = []
    for line in watched_market_data:

        while bearish_market_data[bearish_idx]["date"] < line["date"]:
            bearish_idx += 1

        while bullish_market_data[bullish_idx]["date"] < line["date"]:
            bullish_idx += 1

        while indicator_data[indicator_idx]["date"] < line["date"]:
            indicator_idx += 1

        if not bearish_market_data[bearish_idx]["price"] or \
           not bearish_market_data[bearish_idx - 1]["price"] or \
           not bullish_market_data[bullish_idx]["price"] or \
           not bullish_market_data[bullish_idx - 1]["price"] or \
           not indicator_data[indicator_idx]["value"] or \
           not indicator_data[indicator_idx - 1]["value"]:
            continue

        result.append({
            "date":
            line["date"].isoformat(),
            "watched":
            line["price"],
            "bearish":
            utils.estimators.calculate_third_point(
                bearish_market_data[bearish_idx],
                bearish_market_data[bearish_idx - 1], line["date"]),
            "bullish":
            utils.estimators.calculate_third_point(
                bullish_market_data[bullish_idx],
                bullish_market_data[bullish_idx - 1], line["date"]),
            "indicator":
            utils.estimators.calculate_third_point(
                indicator_data[indicator_idx],
                indicator_data[indicator_idx - 1], line["date"])
        })

    with open(sys.argv[2], "w") as output_file:
        json.dump(result, output_file, indent=4)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
