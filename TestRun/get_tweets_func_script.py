

def get_tweet_frame(target_term):
    import pandas as pd
    import tweepy
    import time
    import json
    from pprint import pprint
    import os
    import numpy as np
    import datetime
    import pytz
    utc=pytz.UTC


    import random
    from twitter_config import consumer_key, consumer_key_secret, access_token, access_token_secret


    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()

    # Additional dependencies from Karthik
    import json
    import csv
    import requests
    # Google developer API key
    from gAPI import gAPIkey as gkey

    startTime = datetime.datetime.now()



    print(gkey)

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


    # find ID of most recent tweet as a starting point for pagination
    public_tweets = api.search(target_term, count=1, result_type="recent")
    for tweet in public_tweets['statuses']:
        oldest_tweet = tweet['id']

    # lists for dataframe
    tweetList = []
    tweetTimes = []
    tweetIDs = []
    tweetCom = []
    tweetNeg = []
    tweetNeu = []
    tweetPos = []
    targetList = []
    locationList = []
    #geo lists
    cities = []
    latitudes = []
    longitudes = []
    coordinates = []

    

    for x in range(3):
        public_tweets = api.search(target_term, count=20, result_type="recent", max_id = oldest_tweet)
    #     time.sleep(10)   # 6 seconds >> 180 requests per 15 mins
        for tweet in public_tweets['statuses']:
    #         pprint(tweet)
            text = tweet['text']
            location = tweet['user']['location']
            results = analyzer.polarity_scores(text)
            locationList.append(location)
            tweetTimes.append(tweet['created_at'])
            tweetList.append(text)
            tweetCom.append(results['compound'])
            tweetNeg.append(results['neg'])
            tweetNeu.append(results['neu'])
            tweetPos.append(results['pos'])            
            targetList.append(target_term)
            tweetIDs.append(tweet['id'])
 

            # Karthik's code:
            target_url = "https://maps.googleapis.com/maps/api/geocode/json"
            qparams = {
                'address': location,
                'key': gkey
            }
            
            geo_data = requests.get(target_url, params=qparams).json()
            

            try:
                lat = geo_data["results"][0]["geometry"]["location"]["lat"]
                lng = geo_data["results"][0]["geometry"]["location"]["lng"]   
                #Lat and Lng exist then append to list
                if lat and lng:
                    latitudes.append(geo_data["results"][0]["geometry"]["location"]["lat"])
                    longitudes.append (geo_data["results"][0]["geometry"]["location"]["lng"])
                    coordinates.append(f'{lat}, {lng}')
            #Append NaN for invalid location
                else: 
                    latitudes.append('NaN')
                    longitudes.append('NaN')
                    coordinates.append('NaN')
            except IndexError:
                    latitudes.append('NaN')
                    longitudes.append('NaN')
                    coordinates.append('NaN')


            if oldest_tweet > tweet['id']:
                oldest_tweet = tweet['id']-1


    # save lists as a dataframe
    tweetFrame = pd.DataFrame({
        'Tweet' : tweetList,
        'Compound': tweetCom,
        'Positive': tweetPos,
        'Negative': tweetNeg,
        'Neutral': tweetNeu,
        'target': targetList,
        'time': tweetTimes,
        'tweet_ID': tweetIDs,
        'tweet_location': locationList,
        'latitudes': latitudes,
        'longitudes': longitudes,
        'coordinates': coordinates    
    })


    endTime = datetime.datetime.now()


    strt = f"{startTime.month}-{startTime.day}-{startTime.year}_{startTime.hour}-{startTime.minute}"
    end = f"{endTime.month}-{endTime.day}-{endTime.year}_{endTime.hour}-{endTime.minute}"

    tweetFrame = tweetFrame[(tweetFrame.coordinates != 'NaN')]

    outputFile = os.path.join('Outputs', f'{target_term}_TweetFile_{strt}___{end}.csv')
    tweetFrame.to_csv(outputFile)
    return tweetFrame


# print(get_tweet_frame('Giraffe'))

# from get_tweets_func_script import get_tweet_frame

# get_tweet_frame('search for this')