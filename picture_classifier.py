'''subscription_key = '{832967259b2c4d10885a398ccbec33cf}'
body_ = '{https://crazyfacemakers.files.wordpress.com/2013/03/mg_9478.jpg}'

####################################

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body_, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))'''


import json
def get_photo_happiness(data):
    happiness = []
    for i in data:
        happiness.append(i['scores']['happiness'] + i['scores']['surprise']-i['scores']['sadness'] - i['scores']['anger'])
    return happiness


with open('details.json','r') as file:
    data = json.load(file)
happiness = get_photo_happiness(data)







####################################