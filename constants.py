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
    'president': ['politics'],
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
    'virus' : ['covid'],
    # 'pizzagate': [] # i think its kinda funny
    'bill gates' : ['technology'],
    'inflation': ['economy'],
    'money': ['economy'],
    'media': ['technology'],
    'video': ['technology'],
    'news': ['technology'],
    'youtube': ['technology'],
    'blog': ['technology'],
}
