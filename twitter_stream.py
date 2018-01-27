import tweepy

# add own details in separate .py file or directly here:
# from twitter_auth import *
# OR
# consumer_key = '*************************'
# consumer_secret = '**************************************************'
# access_token = '**************************************************'
# access_token_secret = '*********************************************'

# authorise api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        status_info = {}

        status_info['text'] = status.text
        status_info['screen_name'] = status.user.screen_name
        status_info['profile_image'] = status.user.profile_image_url_https

        if 'media' in status.entities:
            status_info['url'] = status.entities['media'][0]['media_url']
        else:
            status_info['url'] = ''

        for info in status_info.items():
            print(info[0] + ':', info[1])
        print('\n')

        return status_info

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['python'])
