import requests


df_data = {
  "responseId": "ea3d77e8-ae27-41a4-9e1d-174bd461b68c",
  "session": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0",
  "queryResult": {
    "queryText": "user's original query to your agent",
    "parameters": {
      "geo-city": "Kharkiv"
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Text defined in Dialogflow's console for the intent that was matched",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Text defined in Dialogflow's console for the intent that was matched"
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0/contexts/generic",
        "lifespanCount": 5,
        "parameters": {
          "param": "param value"
        }
      }
    ],
    "intent": {
      "name": "projects/your-agents-project-id/agent/intents/29bcd7f8-f717-4261-a8fd-2d3e451b8af8",
      "displayName": "Weather"
    },
    "intentDetectionConfidence": 1,
    "diagnosticInfo": {},
    "languageCode": "en"
  },
  "originalDetectIntentRequest": {}
}

url = "http://localhost:5000/webhook"
response = requests.post(url, json=df_data)