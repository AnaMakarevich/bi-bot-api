#!/usr/bin/env python

# general imports
import json
import os

# project-specific imports
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    # convert request data to json
    req = request.get_json(silent=True, force=True)

    # debug
    print("Request:")
    print(json.dumps(req, indent=4))

    # process request
    result = process_request(req)

    result = json.dumps(result, indent=4)

    response = make_response(result)
    response.headers['Content-Type'] = 'application/json'
    return response


def process_request(req_json):
    # TODO: check what intent was matched and do the necessary processing
    if req_json.get("queryResult").get("intent").get("displayName") != "Weather":
        print("Intent not recognized")
        return {}
    result = make_olap_query(req_json)

    res = make_webhook_result(result)
    return res


def make_olap_query(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return {'res': 'Fail'}

    return {"res": "Success", "city": city}


def make_webhook_result(data):

    text = "The result is: " + data["res"] + " for city " + data["city"]

    print("Response:")
    print(text)

    return {
        "fulfillmentText": text,
        "source": "bi-bot-api",
        "payload": {
            "slack": {
                "text": text
            },
            "telegram": {
                "text": text
            }
        },
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
