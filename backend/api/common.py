#!/usr/bin/python3

from datetime import datetime
from flask_restful import reqparse

import filters.factory

DATE_TIME_FORMAT = ""


def convert_date_time(date_string):
    return datetime.strptime(date_string, DATE_TIME_FORMAT)


def get_sma(values, ma_type, ma_len, value_name):
    ma_filter = filters.factory.FilterFactory.create(ma_type, ma_len)

    result = []
    for row in values:
        ma_filter.put(row[value_name])
        filtered = ma_filter.get()
        if filtered:
            row[value_name] = filtered
            result.append(row)

    return result


def get_default_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('market', type=str, required=True)
    parser.add_argument('start_date', type=convert_date_time)
    parser.add_argument('end_date', type=convert_date_time)
    parser.add_argument('limit', type=int, default=-1)
    parser.add_argument('step', type=int, default=1)
    parser.add_argument('ma_type', type=str, default="sma")
    parser.add_argument('ma_length', type=int, default=-1)

    return parser
