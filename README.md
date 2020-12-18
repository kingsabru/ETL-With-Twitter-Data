# ETL With Twitter Data

## Overview

This project demonstrates how to work with the Twitter API in python. Using the Tweepy library, you can scrap data from Twitter. The project also shows how to Extract, Transform and Load data into a CSV file and a MongoDB database.

## Task

### Part 1

Write a script that downloads tweets data on a specific search topic using the standard search API. The script should contain the following functions:

1. scrape_tweets() that has the following parameters:

    * Search topic
    * The number of tweets to download per request
    * The number of requests  
    
    and returns a dataframe.
2. Save_results_as_csv() that has the following parameters:
    1. the dataframe from the above function  
    And returns a csv file with the following naming format:

    *tweets_downloaded_yymmdd_hhmmss.csv (where ‘yymmdd_hhmmss’ is the current  timestamp)*

The following attributes of the tweets should be extracted:

* Tweet text
* Tweet id
* Source
* Coordinates
* Retweet count
* Likes count
* User info
    - Username
    - Screenname
    - Location
    - Friends count
    - Verification status
    - Description
    - Followers count

Make sure to not include retweets.  
Make sure you the same tweets appearing multiple times in your final csv.

### Part 2

Create a MongoDB database called Tweets_db and store the extracted tweets into a collection named: raw_tweets.

## Pre-requisites

- Twitter Developer Account  
[Apply](https://developer.twitter.com/en/apply-for-access) for a Twitter Developer account if you do not have one. You would need the credentials for working with the Twitter API.
- Twitter API credentials

## Getting Started

The project was developed using:

* Python 3.7.9
* Anaconda (conda)
* Tweepy
* Pymongo
* Pandas

Follow the steps below to setup the project.

### Create environment

Create a conda environment using the command:
```
conda create -n "env-name" python=3.7
```

### Activate environment

Activate the environment using the command:
```
conda activate env-name
```

### Install packages

Install project packages using the command:
```
pip install -r requirements.txt
```

### Store env variables

To store your access credentials (examples: API keys, Database access credentials), follow the steps below:  

1. Duplicate *.env.example* file and create a new file names *.env*
2. Store your access credentials as needed

## Resources

### Documentations

- [Twitter Search API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets)
- [Tweepy Doc](http://docs.tweepy.org/en/latest/index.html)
- [Pymongo Doc](https://pymongo.readthedocs.io/en/stable/)

### Tutorial Articles

- [Scraping Tweets with Tweepy Python - Python in Plain English](https://medium.com/python-in-plain-english/scraping-tweets-with-tweepy-python-59413046e788)
- [How to Scrape More Information From Tweets on Twitter - Towards Data Science](https://towardsdatascience.com/how-to-scrape-more-information-from-tweets-on-twitter-44fd540b8a1f)