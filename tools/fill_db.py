#!/usr/bin/python3

import re
import sys
import logging
import datetime

import config.parser
import storage.client
import storage.indicators
import storage.tickers


def main():
    if len(sys.argv) != 6:
        print("Usage:", sys.argv[0], "<configuration file>", "<log file>",
              "<market>", "<indicator>", "<candle_size>")
        sys.exit(1)

    parser = config.parser.ConfigurationParser()
    parser.read(sys.argv[1])
    log_file_path = sys.argv[2]
    market = sys.argv[3]
    indicator = sys.argv[4]
    candle_size = sys.argv[5]

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

    with open(log_file_path) as log_file:
        for line in log_file:
            matches = re.match(
                r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
                r".*Current (price|state): ([-.0-9]+)", line)
            if matches and matches.groups():
                print(matches.groups())
                utc_date = datetime.datetime.strptime(matches.group(1),
                                                      "%Y-%m-%d %H:%M:%S,%f")
                data_type = matches.group(2)
                value = float(matches.group(3))
                # if data_type == "price":
                #     ticker_storage.add(market, value, utc_date)
                if data_type == "state":
                    indicator_storage.add(market, candle_size, value, utc_date)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
