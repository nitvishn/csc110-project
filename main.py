"""CSC110 Fall 2021 Final Project

Description
===============================

This file contains the methods which generates the deliverables of the project.
Running this as a python program will output the graphs into data/figures

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs
marking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for our materials,
please consult 𝓌𝒽𝑜𝓂𝒷𝓈𝓉#0930 on discord

This file is Copyright (c) 2021 Aaron Ma, Benjamin Liu, Vishnu Nittoor
"""
import datetime
from computations import calculate_total_valence, calculate_popularity, \
    calculate_sentiment, calculate_topic_popularity, get_time_array, \
    posts_in_interval, filter_posts_by_topic, new_cases_at_times
from data_aggregation import load_posts, load_covid_data
from plotting import plot_frequency_time, plot_overall_valence_histogram, \
    plot_sentiments_popularity, plot_popularities, plot_valence_time
from constants import REDDIT_DATA_FILE, COVID_DATA_FILE


def run_popularity_vs_negatively_charged() -> None:
    """
    Generates the chart which plots the popularity of a post against its sentiment.
    """
    posts = load_posts(REDDIT_DATA_FILE)
    popularities = [calculate_popularity(post) for post in posts]
    sentiments = [calculate_sentiment(post) for post in posts]
    plot_sentiments_popularity(
        sentiments, popularities, 'figures/sentiments_popularity.png')


def run_frequency_over_time() -> None:
    """
    Generates the chart which plots the frequency of posts against time
    """
    resolution = datetime.timedelta(weeks=1)
    posts = load_posts(REDDIT_DATA_FILE)
    case_data = load_covid_data(COVID_DATA_FILE)
    timesteps = get_time_array(datetime.datetime(
        2019, 12, 1), datetime.datetime.now(), resolution)
    freqs = []
    cases = new_cases_at_times(case_data, timesteps, resolution)
    for step in timesteps:
        in_interval = posts_in_interval(posts, step, step + resolution)
        freqs.append(len(in_interval))
    plot_frequency_time(freqs, cases, timesteps,
                        "figures/frequency_over_time.png")


def run_valence_over_time() -> None:
    """
    Generates the chart which plots the total valance against time
    """
    resolution = datetime.timedelta(weeks=1)
    posts = filter_posts_by_topic(load_posts(REDDIT_DATA_FILE), 'covid')
    case_data = load_covid_data(COVID_DATA_FILE)
    timesteps = get_time_array(datetime.datetime(
        2019, 12, 1), datetime.datetime.now(), resolution)
    post_valences = []
    cases = new_cases_at_times(case_data, timesteps, resolution)
    for step in timesteps:
        in_interval = posts_in_interval(posts, step, step + resolution)
        post_valences.append(calculate_total_valence(in_interval))
    plot_valence_time(post_valences, cases, timesteps,
                      "figures/valence_over_time.png")


def overall_valence_histogram() -> None:
    """
    Generates a histogram plotting valance across all posts
    """
    posts = load_posts(REDDIT_DATA_FILE)
    valences = [calculate_sentiment(post) for post in posts]
    plot_overall_valence_histogram(valences, "figures/valence_histogram.png")


def run_topics_vs_time(topics: list[str]) -> None:
    """
    Generates a histogram plotting the popularity of various topics over times
    """
    resolution = datetime.timedelta(weeks=1)
    start = datetime.datetime(2019, 12, 1)
    end = datetime.datetime.now()
    posts = load_posts(REDDIT_DATA_FILE)
    times = get_time_array(start, end, resolution)
    # case_data = load_covid_data('')
    topic_popularities = {}
    for topic in topics:
        popularities = []
        for start_value in times:
            relevant_posts = posts_in_interval(
                posts, start_value, start_value + resolution)
            popularities.append(
                calculate_topic_popularity(relevant_posts, topic))
        topic_popularities[topic] = popularities

    case_data = load_covid_data(COVID_DATA_FILE)
    cases = new_cases_at_times(case_data, times, resolution)
    plot_popularities(times, cases, topic_popularities,
                      f'figures/popularities-{"-".join(topics)}.png')


def most_negative_posts() -> None:
    """
    Prints out the titles of the top 10 most negative posts
    """
    posts = load_posts(REDDIT_DATA_FILE)
    sentiment_tuple = [(calculate_sentiment(post), post) for post in posts]
    sentiment_tuple = sorted(sentiment_tuple, key=lambda t: t[0])
    for x in range(10):
        print(sentiment_tuple[x][0], sentiment_tuple[x][1].text)


def most_positive_posts() -> None:
    """
    Prints out the titles of the top 10 most positive posts
    """
    posts = load_posts(REDDIT_DATA_FILE)
    sentiment_tuple = [(calculate_sentiment(post), post) for post in posts]
    sentiment_tuple = sorted(sentiment_tuple, key=lambda t: t[0])
    for x in range(10):
        print(sentiment_tuple[-x][1].text)


if __name__ == "__main__":
    # import python_ta

    # from python_ta.contracts import check_all_contracts

    # check_all_contracts()

    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['computations', 'datetime', 'plotting',
    #                       'data_aggregation', 'constants'],
    #     'disable': ['R1705', 'W1114'],
    #     'allowed-io': ['most_positive_posts', 'most_negative_posts']
    # })

    run_topics_vs_time(['covid', 'vaccine'])
    run_topics_vs_time(['politics', 'technology', 'aliens'])
    overall_valence_histogram()
    run_valence_over_time()
    run_frequency_over_time()
    run_popularity_vs_negatively_charged()
