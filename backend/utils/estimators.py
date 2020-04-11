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


def get_linear_estimation(data, date):
    prev_row = None
    current_row = data[0]

    for row in data:
        prev_row = current_row
        if prev_row == row:
            continue
        current_row = row
        if date >= row["date"]:
            break

    if current_row["date"] == date:
        return current_row[determine_key(current_row)]

    return calculate_third_point(current_row, prev_row, date)
