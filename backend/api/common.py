#!/usr/bin/python3

from datetime import datetime
from flask_restful import reqparse

import filters.factory

DATE_TIME_FORMAT = ""


def convert_date_time(date_string):
    return datetime.strptime(date_string, DATE_TIME_FORMAT)


def filter_results(values, filter_list, value_name):
    complex_filter = filters.factory.FilterFactory.create_complex(filter_list)

    result = []
    for row in values:
        complex_filter.put(row[value_name])
        filtered = complex_filter.get()
        if filtered:
            row[value_name] = filtered
            result.append(row)

    return result


def get_default_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('market', type=str, required=True)
    parser.add_argument('dateSpan', type=dict)
    parser.add_argument('limit', type=int, default=-1)
    parser.add_argument('step', type=int, default=1)
    parser.add_argument('filter', type=dict, action="append")

    return parser
