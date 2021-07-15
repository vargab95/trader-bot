#!/usr/bin/python3

import abc
import typing
import datetime

from storage.interface import StorageInterface
from signals.trading_signal import TradingSignalDescriptor, TradingSignal, TradingSignalPoint


class MongoStorageBase(StorageInterface):
    def __init__(self, db):
        self._db = db
        self._date_key = "date"
        self._value_key = "value"

    def add(self, descriptor: TradingSignalDescriptor, point: TradingSignalPoint) -> None:
        collection = self._get_collection(descriptor)
        collection.insert_one({
            self._date_key:
            datetime.datetime.utcnow() if not point.date else point.date,
            self._value_key:
            point.value
        })

    def get(self, descriptor: TradingSignalDescriptor) -> TradingSignal:
        collection = self._get_collection(descriptor)
        generated_filter = self._generate_filter(descriptor)
        raw_signal = self._fetch_signal(collection, generated_filter)
        raw_signal = self._sort_by_date(raw_signal)

        if descriptor.limit > 0:
            raw_signal = self._limit(raw_signal, descriptor.limit)

        output_signal = self._generate_signal(raw_signal)
        output_signal.descriptor = descriptor

        return output_signal

    def _generate_filter(self, descriptor: TradingSignalDescriptor) -> typing.Dict:
        if descriptor.start_date and descriptor.end_date:
            return {
                self._date_key: {
                    '$gte': descriptor.start_date,
                    '$lt': descriptor.end_date
                }
            }

        if descriptor.start_date:
            return {
                self._date_key: {
                    '$gte': descriptor.start_date,
                }
            }

        if descriptor.end_date:
            return {
                self._date_key: {
                    '$lt': descriptor.end_date
                }
            }

        return None

    @staticmethod
    def _fetch_signal(collection, generated_filter: typing.Dict):
        if generated_filter:
            return collection.find(generated_filter)
        return collection.find()

    def _sort_by_date(self, result):
        return result.sort([(self._date_key, 1)])

    @staticmethod
    def _limit(result, limit: int):
        return result.limit(limit)

    @abc.abstractmethod
    def _generate_signal(self, fetched_signal) -> TradingSignal:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_collection(self, descriptor: TradingSignalDescriptor):
        pass  # pragma: no cover
