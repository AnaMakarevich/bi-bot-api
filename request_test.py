import requests


df_data = {
  "responseId": "21423def-f63e-4167-b5e5-31ce45239284",
  "queryResult": {
    "queryText": "What is the revenue for May, 2017 - August, 2017",
    "parameters": {
      "bm-type": "",
      "date-period": {
        "endDate": "2017-08-31T12:00:00+03:00",
        "startDate": "2017-05-01T12:00:00+03:00"
      },
      "date": ""
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Sorry, could you please rephrase your request?",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Sorry, could you please rephrase your request?"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/biagent-2d987/agent/intents/e82987e7-c512-4057-88ea-39eba0bc56d5",
      "displayName": "Revenue"
    },
    "intentDetectionConfidence": 1,
    "diagnosticInfo": {},
    "languageCode": "en"
  }
}

url = "http://localhost:5000/webhook"
response = requests.post(url, json=df_data)