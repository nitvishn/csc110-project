"""CSC110 Fall 2021 Final Project

Description
===============================

This file contains constants accessed by other parts of the project

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of TAs
marking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for our materials,
please consult 𝓌𝒽𝑜𝓂𝒷𝓈𝓉#0930 on discord

This file is Copyright (c) 2021 Aaron Ma, Benjamin Liu, Vishnu Nittoor
"""

# a list of topics.
TOPICS = [
    'covid',
    'vaccine',
    'politics',
    'economy',
    'aliens',
    'technology'
]

REDDIT_DATA_FILE = 'data/pushshift-reddit-extracted.json'
COVID_DATA_FILE = 'data/owid-covid-data.json'

# maps keywords to a list containing the topics to which the keyword is correlated.
KEYWORDS = {
    'covid': ['covid'],
    'vaccine': ['covid', 'vaccine'],
    'vaccines': ['covid', 'vaccine'],
    'mask': ['covid'],
    'China': ['politics'],
    'Wuhan': ['politics'],
    'biological warfare': ['covid', 'politics'],
    'aliens': ['aliens'],
    'ufo': ['aliens'],
    'ufos': ['aliens'],
    'covid19': ['covid'],
    'coronavirus': ['covid'],
    'nasa': ['aliens'],
    'president': ['politics'],
    'extraterrestrial': ['aliens'],
    'corona': ['covid'],
    'sightings': ['aliens'],
    'economy': ['economy'],
    'virus': ['covid'],
    'bill gates': ['technology'],
    'inflation': ['economy'],
    'money': ['economy'],
    'media': ['technology'],
    'video': ['technology'],
    'news': ['technology'],
    'youtube': ['technology'],
    'blog': ['technology'],
}


if __name__ == "__main__":

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['math', 'python_ta.contracts', 'hypothesis.strategies'],
        'disable': ['R1705', 'W1114'],
        'allowed-io': []
    })
