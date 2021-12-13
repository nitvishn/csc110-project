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

def load_covid_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['OWID_WRL']
        return data['data']

def new_cases_in_interval(case_data: dict[str, Any], start: datetime.datetime, end: datetime.datetime) -> int:
    return sum([case['new_cases'] for case in case_data if start <= datetime.datetime.strptime(case['date'], "%Y-%m-%d") <= end])

def new_cases_at_times(case_data, times, resolution):
    return [new_cases_in_interval(case_data, time, time + resolution) for time in times]


if __name__ == "__main__":
    data = load_posts('data/pushshift-reddit-extracted.json')
    print(data[0])