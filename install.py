import sqlite3


conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE users(user_id INTEGER PRIMARY KEY, username TEXT, followed_date DATE)''')
cursor.execute('''CREATE TABLE tweets(tweet_id INTEGER PRIMARY KEY, tweet_text TEXT, liked_tweet INT,
               retweeted_date DATE)''')
conn.commit()
