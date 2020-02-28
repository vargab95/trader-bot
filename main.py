#!/usr/bin/python

import sys
import yaml

from spider import TradingViewSpider

def read_configuration():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<configuration file>")
        sys.exit(1)

    with open(sys.argv[1], "r") as config_file:
        return yaml.safe_load(config_file)

def watch_trading_view(spider, bullish_callback, bearish_callback):
    previous_summary = 0.0
    current_summary = 0.0
    try:
        while True:
            spider.fetch_technical_summary()
            current_summary = spider.get_technical_summary()
            print(current_summary)
            if current_summary > 0.0 and previous_summary < 0.0:
                bullish_callback()
            elif current_summary < 0.0 and previous_summary > 0.0:
                bearish_callback()
            previous_summary = current_summary
            spider.sleep_until_next_data()
    except KeyboardInterrupt:
        return

def handle_change_to_bullish():
    print("Buy bull")

def handle_change_to_bearish():
    print("Buy bear")

def main():
    configuration = read_configuration()
    spider = TradingViewSpider(configuration["market"]["name"], configuration["market"]["period"])
    watch_trading_view(spider, handle_change_to_bullish, handle_change_to_bearish)

if __name__ == "__main__":
    main()
