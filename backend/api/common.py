#!/usr/bin/python3

from datetime import datetime


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
