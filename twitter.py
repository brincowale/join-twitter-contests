from TwitterAPI import TwitterAPI
from random import randint
import re
import time
from datetime import datetime


class Twitter:

    def __init__(self, config):
        self.config = config
        self.regex_username = re.compile("@[a-z0-9A-Z_]*")
        self.twitter = TwitterAPI(config['consumer_key'], config['consumer_secret'], config['access_token_key'],
                                  config['access_token_secret'])

    def search_tweets(self, search_keyword, blacklist_keywords, minimum_retweets, tweets_number=100):
        tweets = self.twitter.request('search/tweets', {
            'q': "{} {} min_retweets:{}".format(search_keyword, blacklist_keywords, minimum_retweets),
            'count': tweets_number
        })
        tweets_list = []
        for item in tweets:
            tweets_list.append(item)
        return tweets_list

    def like_tweet(self, tweet_id):
        return self.twitter.request('favorites/create', {'id': tweet_id})

    def contest_require_like(self, tweet):
        tweet_text = tweet['text'].lower()
        for word in self.config['fav_keywords']:
            if word.lower() in tweet_text:
                return True
        return False

    def unlike_tweet(self, tweet_id):
        return self.twitter.request('favorites/destroy', {'id': tweet_id})

    def get_tweets_from_user_timeline(self, username, minimum_retweets, tweets_number=100, exclude_replies=True):
        tweets = self.twitter.request('statuses/user_timeline', {
            'screen_name': username,
            'count': tweets_number,
            'exclude_replies': exclude_replies
        })
        tweets_list = []
        for tweet in tweets:
            if tweet['retweet_count'] >= minimum_retweets:
                tweets_list.append(tweet)
        return tweets_list

    def follow_user(self, username):
        return self.twitter.request('friendships/create', {'id': username})

    def follow_users_mentioned_in_tweet(self, tweet):
        users = self.regex_username.findall(tweet['text'])
        for user in users:
            self.follow_user(user)

    def unfollow_user(self, username):
        return self.twitter.request('friendships/destroy', {'id': username})

    def retweet(self, tweet_id):
        return self.twitter.request('statuses/retweet/:{}'.format(tweet_id))

    def unretweet(self, tweet_id):
        return self.twitter.request('statuses/unretweet/:{}'.format(tweet_id))

    def publish_tweet(self, text_tweet):
        return self.twitter.request('statuses/update', {'status': text_tweet})

    def publish_random_tweets_copied_from_users(self):
        random_user_int = randint(0, len(self.config['copy_tweets_from_users']) - 1)
        tweets = self.get_tweets_from_user_timeline(self.config['copy_tweets_from_users'][random_user_int],
                                                    self.config['minimum_retweets'])
        random_tweet_int = randint(0, len(tweets) - 1)
        self.publish_tweet(tweets[random_tweet_int]['text'])

    def remove_tweet(self, tweet_id):
        return self.twitter.request('statuses/destroy/:{}'.format(tweet_id))

    def valid_tweet(self, tweet):
        tweet_time = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        old_tweet = datetime.now() - datetime.strptime(tweet_time, '%Y-%m-%d')
        if old_tweet.days > self.config['maximum_days_old_tweet']:
            return False
        tweet_text = tweet['text'].lower()
        for word in self.config['blacklisted_words_in_tweet']:
            if word.lower() in tweet_text:
                return False
        username_tweet = tweet['user']['screen_name'].lower()
        try:
            # only when the tweet is a retweet, check the original user and the retweeter
            username_retweet = tweet['retweeted_status']['user']['screen_name'].lower()
        except KeyError:
            username_retweet = None
        for user in self.config['blocked_users']:
            user = user.lower()
            if user == username_tweet or user == username_retweet:
                return False
        user_location = tweet['user']['location'].lower()
        for country in self.config['blacklisted_countries']:
            if country.lower() in user_location:
                return False
        return True

    def contest_tweet(self, tweet):
        tweet_text = tweet['text'].lower()
        for query_retweet in self.config['search_queries'][0]:
            query_retweet = query_retweet.lower()
            for query_contest in self.config['search_queries'][1]:
                if query_retweet in tweet_text and query_contest.lower() in tweet_text:
                    return True
        return False
