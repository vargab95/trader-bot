import sys
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# initialization
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)


@app.route('/api/markets/<path:market>/candles_old', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def relay_candle_request(market):
    response = requests.get(f"https://ftx.com/api/markets/{market}/candles?{request.query_string.decode('utf-8')}")
    print(f"https://ftx.com/api/markets/{market}/candles?{request.query_string}")

    result = jsonify(response.json())
    result.status_code = response.status_code

    return result


@app.route('/api/markets/<path:market>/candles', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def relay_candle_request_with_infinite_limit(market):
    start_time = request.args.get("start_time", None)
    end_time = request.args.get("end_time", None)
    resolution = request.args.get("resolution", None)
    limit = int(request.args.get("limit", None))
    max_limit = 5000

    if limit is None or resolution is None:
        result = jsonify({"success": False, "error": "Limit and resolution are mandatory"})
        result.status_code = 400
        return result

    remaining_limit = limit

    url = f"https://ftx.com/api/markets/{market}/candles"
    aggregated_data = {
        "success": True,
        "result": []
    }

    while remaining_limit > 0:
        data = {
            "resolution": resolution,
            "limit": remaining_limit if remaining_limit < max_limit else max_limit
        }

        if start_time is not None:
            data["start_time"] = start_time

        if end_time is not None:
            data["end_time"] = end_time

        response = requests.get(url, params=data)
        print(url, data)

        if response.status_code != 200:
            result = jsonify({"success": False, "error": "FTX error"})
            result.status_code = response.status_code
            return result

        aggregated_data["result"] = response.json()["result"] + aggregated_data["result"]

        remaining_limit -= max_limit
        start_time = datetime.fromisoformat(response.json()["result"][0]["startTime"])
        end_time = int((start_time - timedelta(seconds=1)).timestamp())
        start_time = None

    result = jsonify(aggregated_data)
    result.status_code = 200

    return result


if __name__ == '__main__':
    app.run(sys.argv[1])
