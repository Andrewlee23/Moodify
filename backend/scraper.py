import os
import requests
import snscrape.modules.twitter as sntwitter
import praw
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
load_dotenv()

API_URL = "http://127.0.0.1:8000/predict"  
def scrape_twitter_top(n=20):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("lang:en").get_items()):
        if i >= n:
            break
        tweets.append(tweet.content) 
    return tweets
def scrape_reddit_top(n=20):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    posts = []
    for submission in reddit.subreddit("all").hot(limit=n):
        posts.append(submission.title) 
    return posts
def analyze_posts(posts, source):
    results = []
    for post in posts:
        try:
            response = requests.post(API_URL, json={"text": post})
            if response.status_code == 200:
                mood = response.json()
                results.append({
                    "text": post,
                    "mood": mood["label"],
                    "source": source
                })
        except Exception as e:
            print(f"Error analyzing: {e}")
    return results

def run_scraper():
    print("Running scraper...")

    tweets = scrape_twitter_top()
    reddit_posts = scrape_reddit_top()

    tweet_results = analyze_posts(tweets, "twitter")
    reddit_results = analyze_posts(reddit_posts, "reddit")

    print("Twitter:", tweet_results[:3])  # preview first 3
    print("Reddit:", reddit_results[:3])
if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scraper, "interval", minutes=30)  # or hours=1
    print(" Scraper running every 30 minutes...")
    run_scraper()  # run once at start
    scheduler.start()
