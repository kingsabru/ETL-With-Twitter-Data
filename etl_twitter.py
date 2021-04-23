import json
import os
import sys
import time

import pandas as pd
import numpy as np
import tweepy
from decouple import UndefinedValueError, config
from pymongo import MongoClient

# TODO: change file name from etl_twitter to script.py

class ETL:
    def __init__(self, api_obj:object):
        self.api = api_obj

    def scrape_tweets(self, query:str, tweets_per_request:int, max_requests:int):
        tweets_list = []

        for i in range(0, max_requests):
            response = tweepy.Cursor(self.api.search, q=query, lang='en', tweet_mode='extended').items(tweets_per_request)
        
            tweets_list = tweets_list + [tweet for tweet in response]
        
        return tweets_list

    def extract(self, tweets:list):
        tweets_df = pd.DataFrame(columns=[
            'tweet',
            'id',
            'source',
            'coordinates',
            'retweetCount',
            'likeCount',
            'username',
            'screenName',
            'location',
            'friendsCount',
            'verificationStatus',
            'description',
            'followersCount'])

        for tweet in tweets:
            if not hasattr(tweet, 'retweeted_status'):
                text = tweet.full_text
                id = tweet.id_str
                source = tweet.source
                coordinates = tweet.coordinates
                retweetCount = tweet.retweet_count
                likeCount = tweet.user.favourites_count
                username = tweet.user.name
                screenName = tweet.user.screen_name
                location = tweet.user.location
                friends = tweet.user.friends_count
                verification = tweet.user.verified
                description = tweet.user.description
                followers = tweet.user.followers_count

                ith_tweet = [text, id, source, coordinates, retweetCount, likeCount, username, screenName, location, friends, verification, description, followers]

                tweets_df.loc[len(tweets_df)] = ith_tweet
        
        return tweets_df

    def save_to_csv(self, df):
        path = os.getcwd() + '\data\\'
        current_timestamp = time.strftime("%y%m%d_%H%M%S")
        
        if not os.path.exists(path):
            os.mkdir(path)
            
        filename = 'tweets_downloaded_' + current_timestamp + '.csv'
        
        fullname = os.path.join(path, filename)
        
        df.to_csv(fullname, index=False)

        return fullname

class MongoDB:
    def __init__(self, db_name, db_password):
        self.db_name = db_name
        self.db_password = db_password

    # TODO: implement function to store csv data to mongodb
    def save_csv_to_db(self, csv):
        pass

    def save_to_db(self, df):
        client = MongoClient('mongodb+srv://kingsabru:{0}@cluster0.cz8qq.gcp.mongodb.net/{1}?retryWrites=true&w=majority'.format(self.db_password, self.db_name))

        db = client.get_database(self.db_name)
        coll = db.raw_tweets
        
        json_data = json.loads(df.to_json(orient='records'))
        
        coll.insert_many(json_data)

def main():
    # retrieve api keys
    if (os.path.isfile(".env")):
        try:
            consumer_key = config('API-KEY')
            consumer_secret = config('API-SECRET-KEY')
            access_token = config('ACCESS-TOKEN')
            access_token_secret = config('ACCESS-TOKEN-SECRET')
        except UndefinedValueError as e:
            print(e , "Check env file.")
            sys.exit(-1)
        else: 
            print("API keys retrieved successfully.")
    else: 
        print("API keys cannot be retrieved. env file does not exist.")
        sys.exit(-1)

    # authenticate user
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    if(not api):
        print("Authentication failed!")
        sys.exit(-1)

    print("Authentication successful.")

    etl= ETL(api)

    query = "Messi"
    tweets_no = 50
    requests_no = 1

    print("Scraping tweets...")
    response = etl.scrape_tweets(query=query, tweets_per_request=tweets_no, max_requests=requests_no)
    print("{} tweets scraped".format(len(response)))

    print("Extracting tweets...")
    extracted_data = etl.extract(response)
    print("{} tweets extratcted".format(len(extracted_data)))

    print("Saving tweets to CSV...")
    saved_path = etl.save_to_csv(extracted_data)
    print("Tweets saved to {}".format(saved_path))

    # saving to database
    print("Saving tweets to MongoDB...")
    db_name = config('DB-NAME')
    db_password = config('DB-PASSWORD')
    print("Database credentials retrieved successfully.")

    mongo_db = MongoDB(db_name, db_password)
    mongo_db.save_to_db(extracted_data)
    print("Tweets saved to database successfully")


if __name__ == "__main__":
    main()