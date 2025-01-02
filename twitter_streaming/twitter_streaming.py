import os
import requests
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import urlencode
import time

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("Twitter BEARER_TOKEN not set in .env file")

client = MongoClient("mongodb://mongodb:27017/")
db = client.twitter
collection = db.tweets

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

def search_tweets(query, max_results=10):
    """Search recent tweets using Twitter API v2."""
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "id,text,created_at,author_id",
    }
    url = f"{SEARCH_URL}?{urlencode(params)}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tweets: {e}")
        return []

    tweets = response.json().get("data", [])
    if tweets:
        collection.insert_many(tweets)
        print(f"Inserted {len(tweets)} tweets into MongoDB.")
    return tweets

def main():
    query = "keyword1 OR keyword2"  
    while True:
        try:
            print("Fetching tweets...")
            search_tweets(query, max_results=10)
            time.sleep(60)  
        except KeyboardInterrupt:
            print("Terminating script...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(60)  

if __name__ == "__main__":
    main()
