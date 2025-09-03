import os
import time
import praw
import tweepy
import sqlite3
import requests
from dotenv import load_dotenv

# Load env
load_dotenv()

# --- Reddit Setup ---
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

DB_PATH = "scraped.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    title TEXT,
    timestamp TEXT,
    prediction TEXT
)
""")
conn.commit()

def save_post_to_db(post, prediction):
    cursor.execute(
        "INSERT INTO posts (source, title, timestamp, prediction) VALUES (?, ?, ?, ?)",
        (post["source"], post["title"], str(post["timestamp"]), prediction)
    )
    conn.commit()

def send_to_ml_api(text):
    url = os.getenv("ML_API_URL")
    try:
        res = requests.post(url, json={"text": text})
        if res.status_code == 200:
            return res.json().get("label", "unknown")
        return "error"
    except Exception as e:
        print("ML API error:", e)
        return "error"
def scrape_reddit_top(limit=20):
    results = []
    for post in reddit.subreddit("all").hot(limit=limit):
        results.append({
            "source": "reddit",
            "title": post.title,
            "timestamp": post.created_utc
        })
    return results

def scrape_twitter_top(limit=20):
    query = "lang:en -is:retweet"
    tweets = twitter_client.search_recent_tweets(
        query=query,
        max_results=limit,
        tweet_fields=["created_at", "text"]
    )
    results = []
    if tweets.data:
        for tweet in tweets.data:
            results.append({
                "source": "twitter",
                "title": tweet.text,
                "timestamp": tweet.created_at
            })
    return results
def run_scraper():
    print("Scraper running...")
    posts = scrape_reddit_top() + scrape_twitter_top()
    for post in posts:
        pred = send_to_ml_api(post["title"])
        save_post_to_db(post, pred)
        print(f"[{post['source']}] {post['title']} -> {pred}")

if __name__ == "__main__":
    while True:
        run_scraper()
        print("Sleeping 30 minutes...")
        time.sleep(1800)
