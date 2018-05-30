import requests


df_data = {
  "responseId": "85b2c295-231a-48a8-a94b-7a2ab58909f8",
  "queryResult": {
    "queryText": "Compare active users: June 2016 to June 2017 for iOS",
    "parameters": {
      "date-period": {
        "endDate": "2017-06-30T12:00:00+03:00",
        "startDate": "2016-06-01T12:00:00+03:00"
      },
      "registered": "",
      "platform_name": [
        "iOS"
      ],
      "compare": "compare",
      "user_visitor": [],
      "date": ""
    },
    "allRequiredParamsPresent": True,
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/biagent-2d987/agent/intents/7d8e88d6-c2b2-4b29-abdb-8494ce9bdf3f",
      "displayName": "Users"
    },
    "intentDetectionConfidence": 0.86,
    "diagnosticInfo": {},
    "languageCode": "en"
  }
}

url = "http://localhost:5000/webhook"
response = requests.post(url, json=df_data)