#!/usr/bin/python3

from datetime import datetime
from flask_restful import reqparse

DATE_TIME_FORMAT = ""


def convert_date_time(date_string):
    return datetime.strptime(date_string, DATE_TIME_FORMAT)


def get_sma(values, sma_len, value_name):
    sma = []

    result = []
    for row in values:
        if row[value_name]:
            sma.append(row[value_name])
        if len(sma) > sma_len:
            sma.pop(0)
            row[value_name] = sum(sma) / len(sma)
            result.append(row)

    return result


def get_default_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('market', type=str, required=True)
    parser.add_argument('start_date', type=convert_date_time)
    parser.add_argument('end_date', type=convert_date_time)
    parser.add_argument('limit', type=int, default=-1)
    parser.add_argument('sma', type=int, default=-1)
    parser.add_argument('step', type=int, default=1)

    return parser
