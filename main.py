#!/usr/bin/python

import sys
import yaml

import spider

def read_configuration():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    with open(sys.argv[1], "r") as config_file:
        return yaml.safe_load(config_file)

def watch_trading_view(tv_spider, bullish_callback, bearish_callback):
    while True:
        try:
            tv_spider.fetch_technical_summary()
            break
        except spider.CannotFetchDataException:
            continue

    previous_summary = tv_spider.get_technical_summary()
    current_summary = 0.0
    try:
        while True:
            try:
                tv_spider.fetch_technical_summary()
            except spider.CannotFetchDataException:
                continue

            current_summary = tv_spider.get_technical_summary()

            print(current_summary)
            if current_summary == 0.0 and previous_summary == 0.0:
                pass
            if current_summary >= 0.0 and previous_summary <= 0.0:
                bullish_callback()
            elif current_summary <= 0.0 and previous_summary >= 0.0:
                bearish_callback()

            previous_summary = current_summary

            tv_spider.sleep_until_next_data()
    except KeyboardInterrupt:
        return

def handle_change_to_bullish():
    print("Buy bull")

def handle_change_to_bearish():
    print("Buy bear")

def main():
    configuration = read_configuration()
    tv_spider = spider.TradingViewSpider(configuration["market"]["name"],
                                         configuration["market"]["candle_size"],
                                         configuration["market"]["check_interval"])
    watch_trading_view(tv_spider, handle_change_to_bullish, handle_change_to_bearish)

if __name__ == "__main__":
    main()
