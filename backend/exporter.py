#!/usr/bin/python3

import sys
import logging
import json

import config.parser
import storage.client
import storage.indicators
import storage.tickers


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
        candle_size=parser.configuration.market.candle_size,
        limit=parser.configuration.database.limit)

    result = []
    max_length = max([
        len(watched_market_data),
        len(bearish_market_data),
        len(bullish_market_data),
        len(indicator_data)
    ])

    for i in range(max_length):
        result.append({
            "watched": watched_market_data[i],
            "bearish": bearish_market_data[i],
            "bullish": bullish_market_data[i],
            "indicator": indicator_data[i]
        })

    for line in result:
        line["watched"]["date"] = line["watched"]["date"].isoformat()
        line["bearish"]["date"] = line["bearish"]["date"].isoformat()
        line["bullish"]["date"] = line["bullish"]["date"].isoformat()
        line["indicator"]["date"] = line["indicator"]["date"].isoformat()

    with open(sys.argv[2], "w") as output_file:
        json.dump(result, output_file, indent=4)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
