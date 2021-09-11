import sys
import json

input_data = json.loads(sys.stdin.read())
filtered_data = list()

for i in range(1, len(input_data)):
    if input_data[i]["AND-ALL-WITH-SWITCHED-RETURN"] != input_data[i - 1]["AND-ALL-WITH-SWITCHED-RETURN"]:
        filtered_data.append([
            input_data[i]["BTC-PERP"],
            input_data[i]["AND-ALL-WITH-SWITCHED-RETURN"]
        ])

print(json.dumps(filtered_data, indent=2))
