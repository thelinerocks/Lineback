
# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your access keys.
# For example, if you obtained your access keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial access keys are generated in the westcentralus region, so if you are using
# a free trial access key, you should not need to change this region.
uri = 'westus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'


import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import requests
import numpy as np


def get_data():
    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'bfe8d2f23e1c40818461bc5b07f4207f',
    }

    params = urllib.parse.urlencode({
    })

    documents = {'documents': [
        {'id': '1', 'language': 'en',
         'text': 'I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable.'},
        {'id': '2', 'language': 'es',
         'text': 'Este ha sido un dia terrible, llegué tarde al trabajo debido a un accidente automobilistico.'}
    ]}
    # Replace the example URL below with the URL of the image you want to analyze.
    try:
        response = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment", headers=headers, params={}, json=documents)
        data = response.json()
        print(data)
    except Exception as e:
        print(e.args)


get_data()
