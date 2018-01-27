import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import requests
import numpy as np

def get_data(url):
    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'cc20f379d1cb429d9a9c7435d6cdbe04',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    body = {'url': url}

    try:
        response = requests.post("https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize", headers=headers, params={}, json=body)
        data = response.json()
        return get_photo_happiness(data)
    except Exception as e:
        print(e.args)

def get_photo_happiness(data):
    happiness = []
    for i in data:
        happiness.append(i['scores']['happiness'] + i['scores']['surprise']-i['scores']['sadness'] - i['scores']['anger'])
    return np.sum(happiness)

with open('details.json','r') as file:
    data = json.load(file)
happiness = get_photo_happiness(data)







####################################