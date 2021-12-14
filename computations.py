"""CSC110 Fall 2021 Final Project

Description
===============================

This file contains methods which compute the various metrics which we assigned to each reddit post. 
It also contains some utility methods used in main

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs 
marking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for our materials,
please consult 𝓌𝒽𝑜𝓂𝒷𝓈𝓉#0930 on discord

This file is Copyright (c) 2021 Aaron Ma, Benjamin Liu, Vishnu Nittoor
"""

from data_aggregation import RedditObject
import datetime
from constants import TOPICS, KEYWORDS
from data_aggregation import RedditObject

from joblib import Memory
memory = Memory("cachedir")

from flair.models import TextClassifier
from flair.data import Sentence
classifier = None


def calculate_popularity(post: RedditObject) -> int:
    """
    Returns the popularity (upvotes - downvotes + number of comments) of a given reddit post. 
    """
    return post.score + post.num_comments


def calculate_relation(post: RedditObject, topic: str) -> float:
    """
    Determines whether a reddit post is related to the given topic or not by scanning for keywords in the post title and body - 1 represents fully related, and 0 represents completely unrelated
    
    Current algorithm - returns 1 if any keywords in the title relate to the topic, 0 otherwise
    """
    combined = post.text
    for keyword in KEYWORDS:
        if keyword in combined and topic in KEYWORDS[keyword]:
            return 1.0
    return 0.0


@memory.cache
def calculate_sentiment_from_text(text: str) -> float:
    """
    Returns the calculated sentiment given a string of text. Sentiment detection is done by Flair. 
    """
    global classifier
    if classifier is None:
        classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(text)
    classifier.predict(sentence)
    multipliers = {
        "POSITIVE": 1,
        "NEGATIVE": -1
    }
    score = sentence.labels[0].score - 0.5
    return multipliers[sentence.labels[0].value] * score


def calculate_sentiment(post: RedditObject) -> float:
    """
    Calculates the sentiment of a reddit object
    """
    combined = post.text
    return calculate_sentiment_from_text(combined)


def posts_in_interval(posts: list[RedditObject], start: datetime.datetime, end: datetime.datetime) -> list[RedditObject]:
    """
    Returns the reddit posts in the given time interval
    """
    return [post for post in posts if start <= post.created_time <= end]


def determine_post_topic(post: RedditObject, threshold: float = 0.5) ->  list[str]:
    """
    Determines the topics to which the given post is related. Threshold provides the minimum degree of relation needed for topics to be related.

    Returns a list of topics.
    """
    return [topic for topic in TOPICS if calculate_relation(post, topic) >= threshold]


def filter_posts_by_topic(posts: list[RedditObject], topic: str) -> list[RedditObject]:
    """
    Filters a list of RedditObjects by the given topic
    """
    return [post for post in posts if calculate_relation(post, topic) == 1]


def calculate_topic_popularity(posts, topic) -> float:
    """
    Calculates the sum total of popularity across different 
    """
    return sum(calculate_relation(post, topic) for post in posts)


def get_time_array(start: datetime.date, end: datetime.date, resolution: datetime.timedelta) -> list[datetime.date]:
    """
    Generates a list of timestamps from start to end with a step size of resolution
    """
    times = []
    while start + resolution <= end:
        times.append(start)
        start += resolution
    return times


def new_cases_in_interval(case_data: list[tuple[datetime.datetime, int]], start: datetime.datetime, end: datetime.datetime) -> int:
    return sum([case[1] for case in case_data if start <= case[0] <= end])


def new_cases_at_times(case_data, times, resolution):
    return [new_cases_in_interval(case_data, time, time + resolution) for time in times]
    

def calculate_total_valence(posts: list[RedditObject]) -> float:
    """
    Returns the sum total valance across a list of reddit posts
    """
    return sum(calculate_sentiment(post) for post in posts)
