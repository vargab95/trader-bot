#!/usr/bin/python

import sys
import logging
import enum
import traceback

from datetime import datetime

import config.parser
import config.logging
import fetcher.single
import detector.factory
import actions
import exchange.factory
import exchange.interface
import mailing.postman
import mailing.error
import mailing.statistics


class BuyState(enum.Enum):
    NONE = 1
    BULLISH = 2
    BEARISH = 3
    SWITCHING_TO_BULLISH = 4
    SWITCHING_TO_BEARISH = 5


def watch_trading_view(tv_fetcher, rising_edge_detector, controller,
                       exchange_config, sma_length, postman):
    tv_fetcher.safe_fetch()
    current_indicator = 0.0
    state = BuyState.NONE
    sma = list()
    next_time = datetime.today()
    while True:
        tv_fetcher.safe_fetch()
        current_indicator = tv_fetcher.get_technical_indicator()
        sma.append(current_indicator)

        if len(sma) <= sma_length:
            logging.info(
                "Waiting for SMA to be filled. "
                "Current length: %d "
                "Final length: %d ", len(sma), sma_length)
        else:
            sma.pop(0)
            current_indicator = sum(sma) / sma_length
            action = rising_edge_detector.check(current_indicator)

            logging.debug("Detector has returned %s", str(action))
            logging.debug("Current state is %s", str(state))

            if action == actions.TradingAction.SWITCH_TO_BULLISH:
                if state != BuyState.BULLISH:
                    state = BuyState.SWITCHING_TO_BULLISH
            elif action == actions.TradingAction.SWITCH_TO_BEARISH:
                if state != BuyState.BEARISH:
                    state = BuyState.SWITCHING_TO_BEARISH

            logging.debug("New state is %s", str(state))

            if state == BuyState.SWITCHING_TO_BULLISH:
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
                    if controller.buy(exchange_config.bullish_market,
                                      amount_to_buy):
                        state = BuyState.BULLISH
                else:
                    logging.warning(
                        "Cannot buy bull due to insufficient money")

                logging.info("New balance: %s", str(controller.get_balances()))
            elif state == BuyState.SWITCHING_TO_BEARISH:
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
                    if controller.buy(exchange_config.bearish_market,
                                      amount_to_buy):
                        state = BuyState.BEARISH
                else:
                    logging.warning(
                        "Cannot buy bear due to insufficient money")

                logging.info("New balance: %s", str(controller.get_balances()))
            logging.info(
                "Current price: %f",
                controller.get_price(
                    exchange.interface.Market.create_from_string("BTC-USDT")))
            all_money = controller.get_money("USDT")
            logging.info("All money: %f", all_money)
            logging.debug(controller.get_balances())

            current_time = datetime.today()
            if current_time > next_time:
                next_time = current_time.replace(day=current_time.day + 1,
                                                 hour=1,
                                                 minute=0,
                                                 second=0,
                                                 microsecond=0)

                message = mailing.statistics.StatisticsMessage()
                message.compose({"all_money": all_money})
                postman.send(message)

        tv_fetcher.sleep_until_next_data()


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

    tv_fetcher = fetcher.single.TradingViewFetcherSingle(
        parser.configuration.market, parser.configuration.market.candle_size)
    long_term_fetcher = None
    if parser.configuration.market.follower_enabled:
        long_term_fetcher = fetcher.single.TradingViewFetcherSingle(
            parser.configuration.market,
            parser.configuration.market.follower_candle_size)

    rising_edge_detector = detector.factory.DetectorFactory.create(
        parser.configuration.market, long_term_fetcher)

    mailing.message.Message.bot_name = parser.configuration.mail.name
    postman = mailing.postman.Postman(parser.configuration.mail)
    postman.connect()

    try:
        watch_trading_view(tv_fetcher, rising_edge_detector, controller,
                           parser.configuration.exchange,
                           parser.configuration.market.indicator_sma, postman)
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
