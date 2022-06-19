import requests


def get_intent(query):
    try:

        ##########
        # Values to modify.

        # YOUR-APP-ID: The App ID GUID found on the www.luis.ai Application Settings page.
        appId = '380a7e65-f511-4714-9f04-ca0ba4e5cb77'

        # YOUR-PREDICTION-KEY: Your LUIS prediction key, 32 character value.
        prediction_key = '97cf5071ac344a5c8dcd2a829b04968a'

        # YOUR-PREDICTION-ENDPOINT: Replace with your prediction endpoint.
        # For example, "https://westus.api.cognitive.microsoft.com/"
        prediction_endpoint = 'https://ielanguageunderstanding.cognitiveservices.azure.com/'

        # The utterance you want to use.
        utterance = query
        ##########

        # The headers to use in this REST call.
        headers = {
        }

        # The URL parameters to use in this REST call.
        params = {
            'query': utterance,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': prediction_key
        }

        # Make the REST call.
        response = requests.get(
            f'{prediction_endpoint}luis/prediction/v3.0/apps/{appId}/slots/production/predict', headers=headers, params=params)

        # Display the results on the console.
        resp = response.json()['prediction']['topIntent']
        print("Intent detected:", resp)
        return resp

    except Exception as e:
        # Display the error string.
        print(f'{e}')
        return None
