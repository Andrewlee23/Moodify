import os
import praw
import tweepy
import requests
import schedule
import time
import pytz
from datetime import datetime
from predict import get_prediction

API_URL = "http://127.0.0.1:8000/predict/"

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
)

def save_post(platform, text, label):
    payload = {"platform": platform, "text": text, "label": label}
    try:
        r = requests.post(API_URL, json=payload)
        r.raise_for_status()
    except Exception as e:
        print("Failed to save post:", e)

def scrape_reddit_top(limit=20):
    posts = []
    try:
        for submission in reddit.subreddit("all").hot(limit=limit):
            posts.append(submission.title)
    except Exception as e:
        print("Reddit scrape failed:", e)
    return posts

def scrape_twitter_top(limit=20):
    posts = []
    try:
        trends = twitter_client.get_place_trends(1)  
        for t in trends[0]["trends"][:limit]:
            posts.append(t["name"])
    except Exception as e:
        print("Twitter scrape failed:", e)
    return posts

def run_scraper():
    print("🔄 Scraper running...")
    reddit_posts = scrape_reddit_top()
    twitter_posts = scrape_twitter_top()
    for post in reddit_posts:
        label = get_prediction(post)
        save_post("reddit", post, label)
    for post in twitter_posts:
        label = get_prediction(post)
        save_post("twitter", post, label)
    print(f"saved {len(reddit_posts) + len(twitter_posts)} posts.")

def job():
    est = pytz.timezone("US/Eastern")
    now = datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Running daily scrape...")
    run_scraper()

if __name__ == "__main__":
    schedule.every().day.at("00:00").do(job)
    print("Scraper scheduled for midnight EST daily...")
    while True:
        schedule.run_pending()
        time.sleep(30)
