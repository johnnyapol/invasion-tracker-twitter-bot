'''
Created on May 3, 2016

@author: johnnyapol
'''
import tweepy
from tweepy.error import TweepError

class Twitter:
    def __init__(self, _conKey, _conSecret, _accessToken, _secretToken):
        print ("Authenticating with Twitter!")
        creds = tweepy.OAuthHandler(_conKey, _conSecret)
        creds.set_access_token(_accessToken, _secretToken)
        self.tapi = tweepy.API(creds)
    
    def postTweet(self, tweet):
        if len(tweet) > 140:
            raise ValueError("Tweet length must not be greater than 140 characters!")
        print ("Posting tweet: " + tweet) 
        try:
           self.tapi.update_status(tweet)
           print(tweet)
        except TweepError as error:
            print ("Failed to post tweet, a TweepError has occurred.") 
            print ( error )
