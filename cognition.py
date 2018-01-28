import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import requests
import numpy as np
import database
import re

EXPR = r'#theline\s#(?P<match>\S*).*'
PHOTO_API_URL = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
TEXT_API_URL = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

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
        response = requests.post(TEXT_API_URL, headers=headers, params={}, json=documents)
        data = response.json()
        # data = {'documents': [{'score': 0.5, 'id': '1'}], 'errors': []}
        return data['documents'][0]['score']
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
        response = requests.post(PHOTO_API_URL, headers=headers, params={}, json=body)
        data = response.json()
        return get_photo_happiness(data)
    except Exception as e:
        print(e.args)

def get_photo_happiness(data):
    happiness = []
    for i in data:
        happiness.append(i['scores']['happiness'] + i['scores']['surprise']-i['scores']['sadness'] - i['scores']['anger'])
    return np.sum(happiness)

def make_text_analytics_document(id, message):
    text = {}
    text['language'] = 'en'
    text['id'] = str(1)
    text['text'] = message
    return {'documents': [text]}

def find_category(message):
    match = re.search(EXPR, message)
    if match is not None:
        category = match.groups()[0].lower()
        return category
    return 'global'

def analyse_post():
    post = database.read_next_post()
    if post.image_url:
        post.image_emotion = measure_emotion(post.image_url)
    document = make_text_analytics_document(post.id, post.message)
    post.text_sentiment = get_text_sentiment(document)
    post.category = find_category(post.message)
    post.analysed = True
    post.save()

if __name__ == '__main__':
    while True:
        try:
            analyse_post()
        except:
            print('cognition threw an error')
