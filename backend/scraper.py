import os
import praw
import tweepy
import sqlite3
import requests
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ML_API_URL = os.getenv("ML_API_URL")
DB_PATH = "scraper.db"

# Reddit auth
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Twitter auth
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT,
            prediction TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_post(source, content, prediction):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO posts (source, content, prediction) VALUES (?, ?, ?)",
            (source, content, prediction)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save failed: {e}")

def scrape_reddit_top(limit=50):
    posts = []
    try:
        for submission in reddit.subreddit("all").hot(limit=limit):
            posts.append(submission.title)
    except Exception as e:
        print(f"Reddit scrape failed: {e}")
    return posts

def scrape_twitter_top(limit=10):
    posts = []
    try:
        tweets = client.search_recent_tweets(query="*", max_results=50, tweet_fields=["lang"])
        for tweet in tweets.data[:limit]:
            posts.append(tweet.text)
    except Exception as e:
        print(f"Twitter scrape failed: {e}")
    return posts

def get_prediction(post):
    try:
        response = requests.post(
            ML_API_URL,
            json={"text": post},   
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to save post: {response.status_code} {response.reason} for url: {ML_API_URL}")
            return None
    except Exception as e:
        print(f"Prediction request failed: {e}")
        return None

def run_scraper():
    print("Scraper running...")

    reddit_posts = scrape_reddit_top()
    twitter_posts = scrape_twitter_top()

    for post in reddit_posts:
        pred = get_prediction(post)
        if pred:
            save_post("reddit", post, str(pred))

    for post in twitter_posts:
        pred = get_prediction(post)
        if pred:
            save_post("twitter", post, str(pred))

    print(f"Saved {len(reddit_posts) + len(twitter_posts)} posts.")

if __name__ == "__main__":
    init_db()
    print("Scraper scheduled for midnight EST daily...")
    schedule.every().day.at("00:00").do(run_scraper)
    run_scraper()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(30)
