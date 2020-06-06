#!/usr/bin/python3

import sys
import json

import applications.base
import utils.estimators

from signals.trading_signal import IndicatorSignalDescriptor, TickerSignalDescriptor


class ExporterApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self._output_file_path: str

    def _initialize_application_logic(self):
        self._initialize_client()
        self._initialize_storages()

    def _process_command_line_arguments(self):
        if len(sys.argv) != 4:
            print("Usage:", sys.argv[0], "<application>",
                  "<configuration file>", "<output file>")
            sys.exit(1)
        self._configuration_file_path = sys.argv[2]
        self._output_file_path = sys.argv[3]

    def _run_application_logic(self):
        data_to_export = self.__fetch()
        self.__sort(data_to_export)
        normalized = self.__normalize(data_to_export)
        result = self.__compose(normalized)
        self.__write(result)

    def __fetch(self):
        return {
            "watched":
            self._ticker_storage.get(
                TickerSignalDescriptor(market=self._configuration.exchange.watched_market.key,
                                       limit=self._configuration.database.limit)),
            "bearish":
            self._ticker_storage.get(
                TickerSignalDescriptor(market=self._configuration.exchange.bearish_market.key,
                                       limit=self._configuration.database.limit)),
            "bullish":
            self._ticker_storage.get(
                TickerSignalDescriptor(market=self._configuration.exchange.bullish_market.key,
                                       limit=self._configuration.database.limit)),
            "indicator":
            self._indicator_storage.get(
                IndicatorSignalDescriptor(
                    market=self._configuration.trader.market,
                    indicator="all",
                    candle_size=self._configuration.trader.candle_size,
                    limit=self._configuration.database.limit))
        }

    @staticmethod
    def __sort(data_to_export):
        for data in data_to_export.values():
            data.data = sorted(data.data, key=lambda item: item.date)

    def __normalize(self, data):
        normalized = {
            "watched": [],
            "bearish": [],
            "bullish": [],
            "indicator": []
        }

        idx = {"bearish": 0, "bullish": 0, "indicator": 0}
        for line in data["watched"].data:
            self.__update_indices(data, idx, line)

            # if not self.__all_exists(data, idx):
            #     continue

            normalized["watched"].append(line)
            for key in idx:
                normalized[key].append(
                    utils.estimators.calculate_third_point(
                        data[key].data[idx[key]], data[key].data[idx[key] - 1],
                        line.date))

        return normalized

    @staticmethod
    def __update_indices(data, idx, line):
        for key in idx:
            while data[key].data[idx[key]].date < line.date:
                idx[key] += 1

    def __all_exists(self, data, idx):
        bear_exists = self.__check_if_exists(data["bearish"], idx["bearish"],
                                             "price")
        bull_exists = self.__check_if_exists(data["bullish"], idx["bullish"],
                                             "price")
        indicator_exists = self.__check_if_exists(data["indicator"],
                                                  idx["indicator"], "value")
        return bear_exists and bull_exists and indicator_exists

    @staticmethod
    def __check_if_exists(data, idx, key):
        return data[idx][key] and data[idx - 1][key]

    @staticmethod
    def __compose(normalized):
        result = []
        for i in range(len(normalized["watched"])):
            result.append({
                "date": normalized["watched"][i].date.isoformat(),
                "watched": normalized["watched"][i].value,
                "bearish": normalized["bearish"][i],
                "bullish": normalized["bullish"][i],
                "indicator": normalized["indicator"][i]
            })
        return result

    def __write(self, result):
        with open(self._output_file_path, "w") as output_file:
            json.dump(result, output_file, indent=4)
