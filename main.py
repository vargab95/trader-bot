#!/usr/bin/python

import sys
import logging
import json

import config
import spider
import detector
import config
import exchange.factory

def watch_trading_view(tv_spider, crossover_detector, controller):
    tv_spider.safe_fetch()
    previous_summary = tv_spider.get_technical_summary()
    current_summary = 0.0
    try:
        while True:
            tv_spider.safe_fetch()
            current_summary = tv_spider.get_technical_summary()
            crossover_detector.check_crossover(current_summary)
            logging.info("Current price: %f",
                         controller.get_price(exchange.interface.Market.create_from_string("BTC-USDT")))
            tv_spider.sleep_until_next_data()
    except KeyboardInterrupt:
        return

def handle_change_to_bullish():
    logging.info("Buy bull")

def handle_change_to_bearish():
    logging.info("Buy bear")

def configure_logging(config: config.LoggingConfig):
    logging.basicConfig(level=config.level,
                        filename=config.path,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    parser = config.ConfigurationParser()
    parser.read(sys.argv[1])

    controller = exchange.factory.ExchangeControllerFactory.create(parser.configuration)

    configure_logging(parser.configuration.logging)
    logging.debug(str(parser.configuration))

    tv_spider = spider.TradingViewSpider(parser.configuration.market)
    crossover_detector = detector.CrossOverDetector(bullish=handle_change_to_bullish,
                                                    bearish=handle_change_to_bearish)
    watch_trading_view(tv_spider, crossover_detector, controller)

if __name__ == "__main__":
    main()
