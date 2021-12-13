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
    An object that represents a single Reddit post. The text field here simply represents the post title.

    Representational Invariants:

    - num_comments >= 0
    - created_time <= datetime.datetime.now()
    """
    text: str
    score: int
    num_comments: int 
    created_time: datetime.datetime


def clean_title(title: str) -> str:
    """
    Returns the title stripped of all punctuation and in lowercase.

    >>> clean_title('ThE AlIeNs aRe cOmIng! AAHHHHH!!!!!')
    the aliens are coming aahhhhh
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


def load_covid_data(filename: str) -> list[tuple[datetime.datetime, int]]:
    """
    Loads the COVID-19 data in the format specified by the Our World In Data dataset. 

    Returns a list of worldwide 
    """
    with open(filename, 'r') as file:
        data = json.load(file)['OWID_WRL']
        case_data = []
        for entry in data:
            case_data.append((datetime.datetime.strptime(entry['date'], "%Y-%m-%d")), entry['new_cases'])
        return case_data


if __name__ == "__main__":
    print(clean_title('ThE AlIeNs aRe cOmIng! AAHHHHH!!!!!'))
