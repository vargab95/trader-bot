#!/usr/bin/python3


def determine_key(data):
    if "value" in data.keys():
        return "value"
    return "price"


def calculate_third_point(p_0, p_1, date):
    key = determine_key(p_0)
    nominator = p_1[key] - p_0[key]
    denumerator = p_1["date"].timestamp() - p_0["date"].timestamp()
    multiplier = date.timestamp() - p_0["date"].timestamp()
    return (nominator / denumerator) * multiplier + p_0[key]
