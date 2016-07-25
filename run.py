from twitter import Twitter
import json
from db import DB
import time
from random import randint
from TwitterAPI import TwitterRequestError


def main(tweets):
    for tweet in tweets:
        if db.old_tweet(tweet['id']) is False and t.valid_tweet(tweet) and t.contest_tweet(tweet):
            t.retweet(tweet['id'])
            if t.contest_require_like(tweet):
                t.like_tweet(tweet['id'])
                db.retweeted_tweet(tweet['id'], tweet['text'], True)
            else:
                db.retweeted_tweet(tweet['id'], tweet['text'], False)
            t.follow_user(tweet['user']['screen_name'])
            t.follow_users_mentioned_in_tweet(tweet)
            time.sleep(randint(config['seconds_wait_between_tweets'][0],
                               config['seconds_wait_between_tweets'][1]))

with open('config.json', encoding="utf8") as config_file:
    config = json.load(config_file)
t = Twitter(config)
db = DB(config['database_name'])
t.publish_random_tweets_copied_from_users()

for query_retweet in config['search_queries'][0]:
    for query_contest in config['search_queries'][1]:
        query = query_retweet + ' ' + query_contest
        tweets = t.search_tweets(query, config['blacklisted_keywords'], config['minimum_retweets'])
        main(tweets)

for user in config['find_contests_from_users']:
    try:
        tweets = t.get_tweets_from_user_timeline(user, config['minimum_retweets'])
        main(tweets)
    except TwitterRequestError:
        print('Twitter request failed (401): maybe the user has block you')

db.close()
