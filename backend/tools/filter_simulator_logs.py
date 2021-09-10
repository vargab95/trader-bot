import sys
import json

input_data = json.loads(sys.stdin.read())
filtered_data = list()

for i in range(1, len(input_data)):
    if input_data[i]["ftx-BALANCES"]["USDT"] != input_data[i - 1]["ftx-BALANCES"]["USDT"] or \
            ("BTC-PERP" in input_data[i]["ftx-POSITIONS"] and
                input_data[i]["ftx-POSITIONS"]["BTC-PERP"] != input_data[i - 1]["ftx-POSITIONS"]["BTC-PERP"]) or \
            input_data[i]["ftx-FUTURE-LOANS"]["BTC-PERP"] != input_data[i]["ftx-FUTURE-LOANS"]["BTC-PERP"]:
        filtered_data.append(input_data[i - 1])
        filtered_data.append(input_data[i])

print(json.dumps(filtered_data, indent=2))
