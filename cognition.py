import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import requests
import numpy as np

uri = 'westus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'

def get_text_sentiment(documents):
    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'bfe8d2f23e1c40818461bc5b07f4207f',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    try:
        response = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment", headers=headers, params={}, json=documents)
        data = response.json()
    except Exception as e:
        print(e.args)

def measure_emotion(url):
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

def make_text_analytics_document(id, message):
    text = {}
    text['id'] = str(id)
    text['language'] = 'en'
    text['text'] = message
    return text

def analyse_post(self):
    post = database.get_next_post()
    post.image_emotion = measure_emotion(post['url'])
    post.text_sentiment = get_text_sentiment()
