#!/usr/bin/env python

# general imports
import json
import os
import dateutil.parser

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
    valid_intents = ['Weather', 'Revenue', "Users"]
    intent_name = req_json.get("queryResult").get("intent").get("displayName")
    if intent_name not in valid_intents:
        print("Intent not recognized")
        return {}
    if intent_name == "Revenue":
        result = calculate_revenue(req_json)
    elif intent_name == "Users":
        if (req_json.get("queryResult").get("compare") != "") and (req_json.get("queryResult").get("date-period") == ""):
            print("Invalid parameters")
            return {}
        else:
            result = calculate_users(req_json)
    else:
        result = make_olap_query(req_json)

    res = make_webhook_result(result)
    return res


def calculate_users(req):
    template_phrase = "Number of {} for {} is {} {}."
    result = req.get("queryResult")
    parameters = result.get("parameters")
    date_period = parameters.get('date-period')
    date = parameters.get('date')
    platform_names = parameters.get("platform_name") # list
    compare = parameters.get("compare") != ""
    user_visitor = parameters.get("user-visitor") # list
    registered = parameters.get("registered") != ""
    if len(platform_names) != 0:
        platforms = "for platforms: " + str(platform_names)
    else:
        platforms = ""
    if date != "":
        date = dateutil.parser.parse(date)
        date_text = "on " + date.strftime('%b, %d, %Y')
    elif date_period != "":
        start_date = dateutil.parser.parse(date_period.get("startDate"))
        end_date = dateutil.parser.parse(date_period.get("endDate"))
        date_text = "period from " + start_date.strftime('%b, %d, %Y') + " to " + end_date.strftime('%b, %d, %Y')
    else:
        date_text = ""
    if user_visitor is not None:
        if ("user" in user_visitor) and ("visitor" in user_visitor):
            who = "user/visitors"
        elif "visitor" in user_visitor:
            who = "visitors"
        else:
            who = "visitors"
    else:
        who = "users"

    text = ""
    if compare and not registered:
        start_date = dateutil.parser.parse(date_period.get("startDate"))
        end_date = dateutil.parser.parse(date_period.get("endDate"))
        n_users_start = 200
        n_users_end = 400
        text += template_phrase.format(who, start_date.strftime('%b, %d, %Y'), str(n_users_start), platforms)
        text += template_phrase.format(who, end_date.strftime('%b, %d, %Y'), str(n_users_end), platforms)
        dif = round(((n_users_end - n_users_start)/n_users_start)*100, 2)
        if n_users_end > n_users_start:
            trend = "growth"
        else:
            trend = "decrease"
        text += "The {} is {}%".format(trend,str(dif))
        return text
    elif registered:
        n_users_signed_up = 400
        return template_phrase.format("users", date_text, n_users_signed_up, "")
    else:
        n_active_users = 432
        return template_phrase.format(who, date_text, n_active_users, platforms)


def calculate_revenue(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    bm_type = parameters.get('bm-type')
    date_period = parameters.get('date-period')
    date = parameters.get('date')
    text = "The revenue for "
    if bm_type != "":
        print (bm_type)
        text += bm_type + " "
        revenue = 10000.0
    if date_period != "":
        print("Period is not none")
        start_date = dateutil.parser.parse(date_period.get("startDate"))
        end_date = dateutil.parser.parse(date_period.get("endDate"))
        start_date_str = start_date.strftime('%b, %d, %Y')
        end_date_str = end_date.strftime('%b, %d, %Y')
        text += "for the period from " + start_date_str + " to " + end_date_str
        revenue = 10000.0
    if date !="":
        print("Date is not none")
        text += " for the date: " + date
        date = dateutil.parser.parse(date)
        revenue = 10000.0
    revenue = "{:,}".format(revenue)
    text += " is $" + revenue
    return text


def make_olap_query(req):

    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return "The result is Fail"
    text = "The result is: Success for city " + city
    return text


def make_webhook_result(text):

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