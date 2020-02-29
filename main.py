#!/usr/bin/python

import sys
import logging
import json

import config
import spider
import detector
import exchange.factory

def watch_trading_view(tv_spider, crossover_detector):
    tv_spider.safe_fetch()
    previous_summary = tv_spider.get_technical_summary()
    current_summary = 0.0
    try:
        while True:
            tv_spider.safe_fetch()
            current_summary = tv_spider.get_technical_summary()
            crossover_detector.check_crossover(current_summary)
            tv_spider.sleep_until_next_data()
    except KeyboardInterrupt:
        return

def handle_change_to_bullish():
    logging.info("Buy bull")

def handle_change_to_bearish():
    logging.info("Buy bear")

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    parser = config.ConfigurationParser()
    parser.read(sys.argv[1])

    controller = exchange.factory.ExchangeControllerFactory.create(parser.configuration.testing)

    logging.basicConfig(level=parser.configuration.log_level)
    logging.debug(str(parser.configuration))

    tv_spider = spider.TradingViewSpider(parser.configuration.market)
    crossover_detector = detector.CrossOverDetector(bullish=handle_change_to_bullish,
                                                    bearish=handle_change_to_bearish)
    watch_trading_view(tv_spider, crossover_detector)

if __name__ == "__main__":
    main()
