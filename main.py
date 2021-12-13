from computations import calculate_total_valence, calculate_popularity, calculate_sentiment, calculate_topic_popularity, get_time_array, posts_in_interval, filter_posts_by_topic, new_cases_at_times, new_cases_in_interval
from data_aggregation import load_posts, RedditObject, load_covid_data
from plotting import plot_frequency_time, plot_overall_valence_histogram, plot_sentiments_popularity, plot_popularities, plot_valence_time
from typing import Callable
from constants import REDDIT_DATA_FILE, COVID_DATA_FILE
import json
import datetime

from constants import TOPICS


def run_popularity_vs_negatively_charged():
    posts = load_posts(REDDIT_DATA_FILE)
    popularities = [calculate_popularity(post) for post in posts]
    sentiments = [calculate_sentiment(post) for post in posts]
    plot_sentiments_popularity(sentiments, popularities, 'figures/sentiments_popularity.png')


def run_frequency_over_time():
    resolution=datetime.timedelta(weeks=1)
    posts = load_posts(REDDIT_DATA_FILE)
    case_data = load_covid_data(COVID_DATA_FILE)
    timesteps = get_time_array(datetime.datetime(2019, 12, 1), datetime.datetime.now(), resolution)
    freqs = []
    cases = new_cases_at_times(case_data, timesteps, resolution)
    for step in timesteps:
        in_interval = posts_in_interval(posts, step, step + resolution)
        freqs.append(len(in_interval))
    plot_frequency_time(freqs, cases, timesteps, "figures/frequency_over_time.png")

def run_valence_over_time():
    resolution=datetime.timedelta(weeks=1)
    posts = filter_posts_by_topic(load_posts(REDDIT_DATA_FILE), 'covid')
    case_data = load_covid_data(COVID_DATA_FILE)
    timesteps = get_time_array(datetime.datetime(2019, 12, 1), datetime.datetime.now(), resolution)
    post_valences = []
    cases = new_cases_at_times(case_data, timesteps, resolution)
    for step in timesteps:
        in_interval = posts_in_interval(posts, step, step + resolution)
        post_valences.append(calculate_total_valence(in_interval))
    plot_valence_time(post_valences, cases, timesteps, "figures/valence_over_time.png")


def overall_valence_histogram():
    posts = load_posts(REDDIT_DATA_FILE)
    valences = [calculate_sentiment(post) for post in posts]
    plot_overall_valence_histogram(valences, "figures/valence_histogram.png")


def run_topics_vs_time(topics):
    resolution = datetime.timedelta(weeks=1)
    start = datetime.datetime(2019, 12, 1)
    end = datetime.datetime.now()
    posts = load_posts(REDDIT_DATA_FILE)
    times = get_time_array(start, end, resolution)
    # case_data = load_covid_data('')
    topic_popularities = dict()
    for topic in topics:
        popularities = []
        for start_value in times:
            relevant_posts = posts_in_interval(posts, start_value, start_value+resolution)
            popularities.append(calculate_topic_popularity(relevant_posts, topic))
        topic_popularities[topic] = popularities
    
    case_data = load_covid_data(COVID_DATA_FILE)
    cases = new_cases_at_times(case_data, times, resolution)
    plot_popularities(times, cases, topic_popularities, f'figures/popularities-{"-".join(topics)}.png')
    

#plot_sentiments_popularity('processed/popularity_charged.json')
# run_frequency_time()

# posts = load_posts(REDDIT_DATA_FILE)
# post = posts[0]
# print(post.created_time)
# print(posts_in_interval(posts, datetime.datetime(2010, 6, 6), datetime.datetime.now()))

def most_negative_posts():
    posts = load_posts(REDDIT_DATA_FILE)
    sentiment_tuple = [(calculate_sentiment(post), post) for post in posts]
    sentiment_tuple = sorted(sentiment_tuple, key= lambda t : t[0])
    for x in range(10):
        print(sentiment_tuple[x][1].text)

# run_frequency_time()
# run_popularity_vs_negatively_charged()
# overall_valence_histogram()
if __name__ == "main":
    run_topics_vs_time(['covid', 'vaccine'])
    run_topics_vs_time(['politics', 'technology', 'aliens'])
    overall_valence_histogram()
    run_valence_over_time()
    run_frequency_over_time()
    run_popularity_vs_negatively_charged()