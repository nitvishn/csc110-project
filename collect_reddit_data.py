import datetime
import requests
import json
import time

def collect_reddit_data():
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
        posts.extend(data)
        start += resolution
        with open('data/pushshift-reddit-extracted.json', 'w') as f:
            json.dump(posts, f)
        time.sleep(1)
    return posts

collect_reddit_data()

python_ta.check_all(config={
    'max-line-length': 100,
    'extra-imports': ['math', 'python_ta.contracts', 'hypothesis.strategies'],
    'disable': ['R1705', 'W1114']
})
    