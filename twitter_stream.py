import tweepy
from tagged_post import *

# add own details in separate .py file or directly here:
from twitter_auth import *
# OR
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

        for info in status_info.items():
            print(info[0] + ':', info[1])
        print('\n')

        save_post(status_info)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['trump'])


time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))