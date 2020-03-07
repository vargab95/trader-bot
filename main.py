#!/usr/bin/python

import sys
import logging

import config.parser
import config.logging
import spider
import detector.factory
import actions
import exchange.factory
import exchange.interface


def handle_change_to_bullish():
    logging.info("Buy bull")


def handle_change_to_bearish():
    logging.info("Buy bear")


def watch_trading_view(tv_spider, crossover_detector, controller,
                       exchange_config):
    tv_spider.safe_fetch()
    current_summary = 0.0
    try:
        while True:
            tv_spider.safe_fetch()
            current_summary = tv_spider.get_technical_summary()
            action = crossover_detector.check(current_summary)
            if action == actions.TradingAction.SWITCH_TO_BULLISH:
                available_amount = controller.get_balance(
                    exchange_config.bearish_market.target)
                if available_amount > 0.0:
                    controller.sell(exchange_config.bearish_market,
                                    available_amount)
                else:
                    logging.warning(
                        "Cannot sell bear due to insufficient amount")

                balance = controller.get_balance(
                    exchange_config.bullish_market.base)
                price = controller.get_price(exchange_config.bullish_market)
                amount_to_buy = balance / price
                if amount_to_buy > 0.0:
                    controller.buy(exchange_config.bullish_market,
                                   amount_to_buy)
                else:
                    logging.warning(
                        "Cannot buy bull due to insufficient money")

                logging.info("New balance: %s", str(controller.get_balances()))
            elif action == actions.TradingAction.SWITCH_TO_BEARISH:
                available_amount = controller.get_balance(
                    exchange_config.bullish_market.target)
                if available_amount > 0.0:
                    controller.sell(exchange_config.bullish_market,
                                    available_amount)
                else:
                    logging.warning(
                        "Cannot sell bull due to insufficient amount")

                balance = controller.get_balance(
                    exchange_config.bearish_market.base)
                price = controller.get_price(exchange_config.bearish_market)
                amount_to_buy = balance / price
                if amount_to_buy > 0.0:
                    controller.buy(exchange_config.bearish_market,
                                   amount_to_buy)
                else:
                    logging.warning(
                        "Cannot buy bear due to insufficient money")

                logging.info("New balance: %s", str(controller.get_balances()))
            logging.info(
                "Current price: %f",
                controller.get_price(
                    exchange.interface.Market.create_from_string("BTC-USDT")))
            logging.info("All money: %f", controller.get_money("USDT"))
            logging.debug(controller.get_balances())
            tv_spider.sleep_until_next_data()
    except KeyboardInterrupt:
        return


def configure_logging(configuration: config.logging.LoggingConfig):
    logging.basicConfig(
        level=configuration.level,
        filename=configuration.path,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    parser = config.parser.ConfigurationParser()
    parser.read(sys.argv[1])
    configure_logging(parser.configuration.logging)
    logging.debug(str(parser.configuration))

    controller = exchange.factory.ExchangeControllerFactory.create(
        parser.configuration)

    tv_spider = spider.TradingViewSpider(parser.configuration.market,
                                         parser.configuration.market.candle_size)
    long_term_spider = None
    if parser.configuration.market.follower_enabled:
        long_term_spider = spider.TradingViewSpider(
            parser.configuration.market,
            parser.configuration.market.follower_candle_size)

    crossover_detector = detector.factory.DetectorFactory.create(
        parser.configuration.market, long_term_spider)

    watch_trading_view(tv_spider, crossover_detector, controller,
                       parser.configuration.exchange)


if __name__ == "__main__":
    main()
