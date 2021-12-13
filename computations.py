from typing import Text
from data_aggregation import RedditObject
import datetime
from constants import TOPICS, KEYWORDS
from data_aggregation import RedditObject

from joblib import Memory
memory = Memory("cachedir")

from nltk.sentiment import SentimentIntensityAnalyzer

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
            return 1
    return 0

@memory.cache
def calculate_sentiment_from_text(text: str) -> float:
    # VADER
    # return sentiment_analyzer.polarity_scores(combined)["compound"]

    # Flair
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
    combined = post.text
    return calculate_sentiment_from_text(combined)


def posts_in_interval(posts: list[RedditObject], start: datetime.datetime, end: datetime.datetime):
    return [post for post in posts if start <= post.created_time <= end]

def determine_post_topic(post: RedditObject, threshold: float = 0.5) ->  list[str]:
    """
    Determines the topics to which the given post is related. Threshold provides the minimum degree of relation needed for topics to be related.

    Returns a list of topics.
    """
    return [topic for topic in TOPICS if calculate_relation(post, topic) >= threshold]

def filter_posts_by_topic(posts, topic):
    return [post for post in posts if calculate_relation(post, topic) == 1]

def calculate_topic_popularity(posts, topic):
    return sum(calculate_relation(post, topic) for post in posts)

def get_time_array(start, end, resolution):
    times = []
    while start + resolution <= end:
        times.append(start)
        start += resolution
    return times

def calculate_average_valence(posts):
    return sum(calculate_sentiment(post) for post in posts)
    return 0 if not posts else sum(calculate_sentiment(post) for post in posts)/len(posts)