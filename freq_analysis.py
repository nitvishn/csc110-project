from data_aggregation import RedditObject, load_posts
import matplotlib.pyplot as plt
from constants import REDDIT_DATA_FILE

from plotting import plot_frequencies

def compute_frequencies(posts: list[RedditObject]):
    freq_dict = {}
    for post in posts:
        for word in post.text.split(' '):
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict

def load_commonly_used_words():
    with open('data/commonly_used_words.txt', 'r') as file:
        words = {word.strip() for word in file}
        return words

def filter_frequencies(freq_dict):
    common = load_commonly_used_words()
    filtered = {}
    for word in freq_dict:
        if word not in common:
            filtered[word] = freq_dict[word]
    return filtered

if __name__ == "__main__":
    posts = load_posts(REDDIT_DATA_FILE)
    freq_dict = compute_frequencies(posts)
    # words, frequencies = zip(*[(key, value) for key, value in freq_dict.items()])
    # plot_frequencies(words, frequencies)

    freq_dict = filter_frequencies(freq_dict)
    sorted_words = sorted(list(freq_dict.keys()), key= lambda x: freq_dict[x], reverse=True)
    for word in sorted_words[:100]:
        print(word, freq_dict[word])
