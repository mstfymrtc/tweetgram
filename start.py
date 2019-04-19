import textblob as textblob
import json
import requests
import os
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob


############# constants ####################

consumer_key=os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"]

access_token=os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

chat_id=os.environ["TELEGRAM_CHAT_ID"]
telegram_api_token=os.environ["TELEGRAM_API_TOKEN"]

url="https://api.telegram.org/bot"+telegram_api_token+"/sendMessage"

############# constants ####################


class StdOutlistener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = TextBlob(all_data["text"])

        all_data['sentiment'] = tweet.sentiment

        print(tweet)
        print(tweet.sentiment)


        requests.post(url,data={"chat_id":chat_id,"text":all_data["text"]})

        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, StdOutlistener())

# track hashtags etc. check https://tweepy.readthedocs.io/en/v3.5.0 
# twitterStream.filter(languages=["en"], track=["Test"])

# track user if posts new tweet with account id 
twitterStream.filter(follow=['546889305'])

