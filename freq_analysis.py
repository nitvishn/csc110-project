"""CSC110 Fall 2021 Final Project

Description
===============================

This file contains methods related to the frequency analysis used whilst
finding good keywords

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


def compute_frequencies(posts: list[RedditObject]) -> dict[str, int]:
    """
    Returns a dictionary mapping each word to the number of times
    it occurs within the contents of a list of reddit posts.
    """
    freq_dict = {}
    for post in posts:
        for word in post.text.split(' '):
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict


def load_commonly_used_words() -> set[str]:
    """
    Loads a list of commonly used words and returns .
    """
    with open('data/commonly_used_words.txt', 'r') as file:
        words = {word.strip() for word in file}
        return words


def filter_frequencies(freq_dict: dict[str, int]) -> dict[str, int]:
    """
    Filters out the commonly used words from the keys of freq_dict.
    """
    common = load_commonly_used_words()
    filtered = {}
    for word in freq_dict:
        if word not in common:
            filtered[word] = freq_dict[word]
    return filtered


if __name__ == "__main__":

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['math', 'python_ta.contracts', 'hypothesis.strategies',
                          'data_aggregation', 'constants'],
        'disable': ['R1705', 'W1114'],
        'allowed-io': ['load_commonly_used_words']
    })
