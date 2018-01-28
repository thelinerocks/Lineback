import tweepy
<<<<<<< HEAD
import json
import os
=======
from tagged_post import *

>>>>>>> jack
# add own details in separate .py file or directly here:
from twitter_auth import *
# OR


consumer_key = 'cfUOK7slPd3UOXx05JEHUi73H'
consumer_secret = '0HKVWiKKg6pruY9nTtWiZIjG0Yu3yuN4S7APAMWHG9IrqKqh3B'
access_token = '1588152001-x6kGJtgFhP8ya7BIJHEfp9GaI2cpMDdLGRvKuB0'
access_token_secret = 'qtIt7gizK69WdLhIzyGvh1oRBOMtpHFvkMrue2V4Ww65s'
# consumer_key = '*************************'
# consumer_secret = '**************************************************'
# access_token = '**************************************************'
# access_token_secret = '*********************************************'

from dateutil import parser
import calendar

def make_timestamp(date):
    #parsed_date = parser.parse(date)
    timestamp = calendar.timegm(parser.parse(date).timetuple())
    return timestamp

# authorise api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        status_info = {}
        #status_info['time_stamp'] = make_timestamp(status.created_at)
        status_info['social_network'] = 'twitter'
        status_info['message'] = status.text
        status_info['user_name'] = status.user.screen_name
        status_info['profile_pic_url'] = status.user.profile_image_url_https
        status_info['location'] = status.user.location

        if 'media' in status.entities:
            status_info['image_url'] = status.entities['media'][0]['media_url']
        else:
            status_info['image_url'] = ''

        if not os.path.exists('twitter'):
            os.makedirs('twitter')
        tweets = os.listdir('twitter')
        numbers = []
        for i in tweets:
            numbers.append(int(i.split('.')[0]))
        numbers = sorted(numbers)
        if len(numbers) > 0:
            count = numbers[-1]+1
        else:
            count = 0
        filename = str(count) + '.json'
        with open(os.path.join('twitter',filename),'w') as file:
            json.dump(status_info,file)

        for info in status_info.items():
            print(info[0] + ':', info[1])
        print('\n')

        save_post(status_info)


def twitter_update_status(self,text = "#LineisLife"):
    api.update_status(status=text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['python'])
