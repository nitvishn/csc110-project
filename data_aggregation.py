import json
from typing import Any
import datetime
from dataclasses import dataclass
import string
from constants import KEYWORDS
import requests
import time

@dataclass
class RedditObject(object):
    """
    An object that represents a single Reddit post.
    """
    text: str
    score: int
    num_comments: int 
    created_time: datetime.datetime


def clean_title(title: str) -> str:
    """
    Returns the title stripped of all punctuation and in lowercase.
    """
    return title.translate(str.maketrans('', '', string.punctuation)).lower()


def load_posts(filename: str) -> list[RedditObject]:
    """
    Loads data from the file given, and assumes that each line of the file contains a JSON object corresponding to a post in the subreddit.

    Returns a list of dictionaries each representing a post.
    """
    
    posts = []
    with open(filename, 'r') as file:
        data = json.load(file)
        for post in data:
            posts.append(RedditObject(clean_title(post['title']), post['score'], post['num_comments'], datetime.datetime.fromtimestamp(post['created_utc'])))
    return posts

def scrape_reddit_data():
    start = datetime.datetime(2010, 12, 1)
    end = datetime.datetime.now()
    resolution = datetime.timedelta(days=5)
    posts = []
    ratelimit = 120
    while start + resolution <= end:
        query = {
            'fields': ['title','num_comments','score','created_utc','body'],
            'before': int((start + resolution).timestamp()),
            'after': int(start.timestamp()),
            'size': 1000,
            'subreddit': 'conspiracies'
        }
        response = requests.get(f"https://api.pushshift.io/reddit/search/submission/", params=query)
        print(response.url)
        data = json.loads(response.text)['data']
        print(f"Completed {start}.")
        posts.append(data)
        start += resolution
        with open('pushshift-reddit.json', 'w') as f:
            json.dump(posts, f)
        time.sleep(1)
    return posts


if __name__ == "__main__":
    data = load_posts('data/pushshift-reddit-extracted.json')
    print(data[0])