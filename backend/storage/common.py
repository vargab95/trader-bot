#!/usr/bin/python3


def sort_and_limit_result(result, limit):
    if limit > 0:
        return result.sort([("date", -1)]).limit(limit)
    return result.sort([("date", 1)])
