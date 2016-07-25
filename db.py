import sqlite3
import datetime


class DB:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)

    def followed_user(self, user_id, username):
        c = self.conn.cursor()
        c.execute('''INSERT INTO users VALUES (?,?,?)''', (user_id, username, datetime.datetime.now()))
        self.conn.commit()

    def old_user(self, user_id):
        c = self.conn.cursor()
        c.execute('''SELECT user_id FROM users WHERE user_id=?''', (user_id,))
        if c.fetchone() is None:
            return False,
        return True

    def update_last_user_contest(self, user_id):
        c = self.conn.cursor()
        c.execute('''UPDATE users SET followed_date=? WHERE user_id=?''', (datetime.datetime.now(), user_id))
        self.conn.commit()

    def retweeted_tweet(self, tweet_id, tweet_text, liked_tweet):
        c = self.conn.cursor()
        c.execute('''INSERT INTO tweets VALUES (?,?,?,?)''', (tweet_id, tweet_text, liked_tweet, datetime.datetime.now()))
        self.conn.commit()

    def old_tweet(self, tweet_id):
        c = self.conn.cursor()
        c.execute('''SELECT tweet_id FROM tweets WHERE tweet_id=?''', (tweet_id,))
        if c.fetchone() is None:
            return False
        return True

    def close(self):
        self.conn.close()
