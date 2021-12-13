import matplotlib.pyplot as plt
import numpy as np
import computations
import json


def plot_frequencies(words: list[str], frequencies: list[int], max_words: int = 50):
    fig, ax = plt.subplots()

    words = words[:max_words]
    frequencies = frequencies[:max_words]

    y_pos = np.arange(len(words))

    ax.barh(y_pos, frequencies, align='center')
    ax.set_yticks(y_pos, labels=words)
    ax.invert_yaxis()  # labels read top-to-bottom

    plt.show()

def plot_sentiments_popularity(sentiments, popularities, save_to_file=False):
    colors = [(s + 0.5) * np.array([-255, 255, 0])/255 + np.array([255, 0, 0])/255 for s in sentiments]
    fig = plt.figure()
    plt.title("")
    plt.xlabel("Valence of the post title ")
    plt.ylabel("Post popularity (score + number of comments)")
    plt.scatter(sentiments, popularities, c = colors, s=2)
    plt.title("Post popularity vs valence of sentiment")
    fig.set_size_inches(9, 6)
    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
    else:
        plt.show()

def plot_frequency_time(post_frequency, cases, times, save_to_file=False):
    fig, axs = plt.subplots(2)
    fig.suptitle('Post frequency analyzed with new cases (each over 7 days)')
    axs[0].plot(times, post_frequency)
    axs[1].plot(times, cases)

    axs[0].set_ylabel('Number of posts (over 7 days)')
    axs[0].set_xlabel('Time')

    axs[1].set_ylabel('New cases (over 7 days)')
    axs[1].set_xlabel('Time')

    fig.set_size_inches(9, 6)
    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
    else:
        plt.show()


def plot_valence_time(post_valences, cases, times, save_to_file=False):
    fig, axs = plt.subplots(2)
    fig.suptitle('Post valence analyzed with new cases (each over 7 days)')
    axs[0].plot(times, post_valences)
    axs[1].plot(times, cases)
    axs[1].set_ylabel('Total post valence (over 7 days)')
    axs[1].set_xlabel('Time')

    axs[1].set_ylabel('New cases (over 7 days)')
    axs[1].set_xlabel('Time')
    fig.set_size_inches(9, 6)
    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
    else:
        plt.show()



def plot_popularities(times, cases, topic_popularities, save_to_file=False):
    fig, axs = plt.subplots(2) #creates a pair of (sub)plots, fig and axs
    fig.suptitle('Topic popularity analyzed with new cases') #gives fig a title
    for topic in topic_popularities:# this loop inserts data
        axs[0].plot(times, topic_popularities[topic], label=topic)
    axs[1].plot(times, cases)#plots time and covid cases?
    axs[0].legend()
    axs[1].set_xlabel('Time')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Topic popularity (over 7 days)')
    axs[1].set_ylabel('New cases (over 7 days)')
    fig.set_size_inches(9, 6)
    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
    else:
        plt.show()


def plot_overall_valence_histogram(valences, save_to_file=False):
    plt.figure()
    plt.title('Distribution of posts according to valence')
    plt.ylabel("Number of posts")
    plt.xlabel("Post valence")
    plt.hist(valences, bins=40)
    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
    else:
        plt.show()