"""CSC110 Fall 2021 Final Project

Description
===============================

This file contains methods related to the aggregation and sanitization of collected data

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs
marking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for our materials,
please consult 𝓌𝒽𝑜𝓂𝒷𝓈𝓉#0930 on discord

This file is Copyright (c) 2021 Aaron Ma, Benjamin Liu, Vishnu Nittoor
"""
import json
import datetime
from dataclasses import dataclass
import string


@dataclass
class RedditObject:
    """
    An object that represents a single Reddit post. The text field here simply represents
    the post title.

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
    Loads data from the file given, and assumes that each line of the file contains a
    JSON object corresponding to a post in the subreddit.

    Returns a list of dictionaries each representing a post.
    """
    posts = []
    with open(filename, 'r') as file:
        data = json.load(file)
        for post in data:
            posts.append(RedditObject(clean_title(
                post['title']), post['score'], post['num_comments'],
                datetime.datetime.fromtimestamp(post['created_utc'])))
    return posts


def load_covid_data(filename: str) -> list[tuple[datetime.datetime, int]]:
    """
    Loads the COVID-19 data in the format specified by the Our World In Data dataset.

    Returns a list of tuples, each representing a day's entry in the worldwide case counts
    """
    with open(filename, 'r') as file:
        data = json.load(file)['OWID_WRL']
        case_data = []
        for entry in data['data']:
            case_data.append((datetime.datetime.strptime(
                entry['date'], "%Y-%m-%d"), entry['new_cases']))
        return case_data


if __name__ == "__main__":

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['math', 'python_ta.contracts', 'hypothesis.strategies',
                          'dataclasses', 'json', 'string', 'datetime'],
        'disable': ['R1705', 'W1114'],
        'allowed-io': ['load_posts', 'load_covid_data']
    })
