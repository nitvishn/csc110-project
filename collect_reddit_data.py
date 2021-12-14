"""
CSC110 Fall 2021 Final Project

Description
===============================
This module contains a method which obtains the reddit posts from the reddit
api and dumps it into a JSON file.

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
import time
import datetime
import requests


def collect_reddit_data() -> None:
    """
    This method collects all reddit posts from the r/consiracy subreddit and outputs the data into a
    JSON file
    """
    start = datetime.datetime(2010, 12, 1)
    end = datetime.datetime.now()
    resolution = datetime.timedelta(days=5)
    posts = []
    while start + resolution <= end:
        query = {
            'fields': ['title', 'num_comments', 'score', 'created_utc', 'body'],
            'before': int((start + resolution).timestamp()),
            'after': int(start.timestamp()),
            'size': 1000,
            'subreddit': 'conspiracies'
        }
        response = requests.get(
            "https://api.pushshift.io/reddit/search/submission/", params=query)
        print(response.url)
        data = json.loads(response.text)['data']
        print(f"Completed {start}.")
        posts.extend(data)
        start += resolution + datetime.timedelta(days=1)
        with open('data/pushshift-reddit-extracted.json', 'w') as f:
            json.dump(posts, f)
        time.sleep(1)


if __name__ == "__main__":

    import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['python_ta.contracts', 'time', 'json', 'requests', 'datetime'],
    #     'disable': ['R1705', 'W1114'],
    #     'allowed-io': ['collect_reddit_data']
    # })

    collect_reddit_data()
