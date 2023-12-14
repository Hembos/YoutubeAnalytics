import logging
import time
from collections import defaultdict

from stop_words import safe_get_stop_words
from wordcloud import WordCloud

from app.emotion_analisis.analyser import Analyser
import numpy as np
"""
Calculates metric -- number of comments depending on publication time
"""

import matplotlib.pyplot as plt
from datetime import datetime, timezone
from collections import Counter


def plot_counts_by_datetime(comments: dict, video_name: str, make_plot: bool = False, return_count=False) -> list:
    # Extract the time information and count occurrences cumulatively
    datetime_counts = Counter()
    for entry in comments.values():
        datetime_entry = datetime.fromisoformat(entry['updatedAt'][:-1])  # Convert to datetime object
        datetime_counts[datetime_entry] += 1

    # Sort the entries by datetime
    sorted_counts = sorted(datetime_counts.items(), key=lambda x: x[0])

    # Extract datetime and cumulative counts
    datetimes = [date for date, _ in sorted_counts]
    counts = [count for _, count in sorted_counts]

    # Perform cumulative sum for the counts
    cumulative_counts = [sum(counts[:i + 1]) for i in range(len(counts))]
    if make_plot:
        plt.figure(figsize=(12, 6))
        plt.plot(datetimes, cumulative_counts, marker='o', linestyle='-')
        plt.xlabel('Date and Time')
        plt.ylabel('Count of comments')
        plt.title(f'Count of comments {video_name}')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        logging.basicConfig(level=logging.INFO,
                            filename="analysis/analysis.log", format="%(asctime)s %(levelname)s %(message)s")
        plt.savefig(f'Comments_count_of_{video_name}.png')
    if return_count:
        return [datetimes, counts]
    return [datetimes, cumulative_counts]


def plot_counts_neg_and_pos(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None or len(analyser.result.values()) > 0\
            and next(iter(analyser.result.values())).get('sentiment') is None:
        d_type = {'sentiment': True}
        analyser.analyse_comments(comments, d_type)
    positive_comments_count = 0
    negative_comments_count = 0
    neutral_comments_count = 0
    for entry in analyser.result.values():
        if entry['sentiment'].output == 'NEG':
            negative_comments_count += 1
        if entry['sentiment'].output == 'POS':
            positive_comments_count += 1
        if entry['sentiment'].output == 'NEU':
            neutral_comments_count += 1
    labels = ['Positive Comments', 'Negative Comments', 'Neutral Comments']
    sizes = [positive_comments_count, negative_comments_count, neutral_comments_count]
    if make_plot:
        colors = ['#66ff66', '#ff6666', '#999999']  # Green for positive, red for negative, gray for neutral
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_neg_and_pos_count_of_{video_name}.png')
    return dict(zip(labels, sizes))


def plot_counts_emotion(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None or len(analyser.result.values()) > 0 and \
            next(iter(analyser.result.values())).get('emotion') is None:
        d_type = {'emotion': True}
        analyser.analyse_comments(comments, d_type)
    types = ['others', 'joy', 'sadness', 'anger', 'surprise', 'disgust', 'fear']
    counts = dict(zip(types, [0] * len(types)))
    for entry in analyser.result.values():
        for t in types:
            if entry['emotion'].output == t:
                counts[t] += 1
    sizes = [i for i in counts.values()]
    if make_plot:
        labels = types
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_emotion_count_of_{video_name}.png')
    return counts


def plot_like_vs_replies_counts(comments: dict, video_name: str, make_plot: bool = False):
    reply_count_dict = defaultdict(int)
    like_count_dict = defaultdict(int)
    for comment_id, comment_info in comments.items():
        is_reply = comment_info.get('isReply', False)
        # like_count = comment_info.get('likeCount', 0)
        parent_id = comment_info.get('parentId', None)
        if is_reply:
            reply_count_dict[parent_id] += 1
    for comment_id in reply_count_dict.keys():
        like_count_dict[comment_id] = comments[comment_id].get('likeCount', 0)
    reply_counts = list(reply_count_dict.values())
    like_counts = list(like_count_dict.values())
    if make_plot:
            plt.scatter(reply_counts, like_counts, color='blue', alpha=0.5)
            plt.title(f'Like Count vs Reply Count {video_name}')
            plt.xlabel('Reply Count')
            plt.ylabel('Like Count')
            plt.savefig(f'Comments_likes_by_replies{video_name}.png')
    return {'reply_count': reply_count_dict, 'like_count': like_count_dict}


def plot_counts_langs(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None or len(analyser.result.values()) > 0 and \
            next(iter(analyser.result.values())).get('lang') is None:
        d_type = {'lang': True}
        analyser.analyse_comments(comments, d_type)
    counts = dict()
    for entry in analyser.result.values():
        if entry['lang'][0]['label'] not in counts.keys():
            counts[entry['lang'][0]['label']] = 0
        counts[entry['lang'][0]['label']] += 1
    sizes = [i for i in counts.values()]
    if make_plot:
        labels = list(counts.keys())
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_neg_and_pos_count_of_{video_name}.png')
    return counts


def plot_word_map(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()  # todo think about what if only two comments
    if analyser.result is None or \
            (len(analyser.result.values()) > 0 and \
             next(iter(analyser.result.values())).get('lang') is None
             and analyser.result.get('sentiment') is None):
        d_type = {'lang': True,
                  'sentiment': True}
        analyser.analyse_comments(comments, d_type)
    # text = analyser.result.pop('word_count')
    text = analyser.result
    counts = set()
    pos_freq = defaultdict(int)
    neg_freq = defaultdict(int)
    freq = defaultdict(int)
    for entry in analyser.result.values():
        sentance = entry['sentiment'].sentence
        words = "".join(c for c in sentance if c.isalnum() or c.isspace())
        words = words.lower().split()
        for word in words:
            freq[word] += 1
            if entry['sentiment'].output == 'POS':
                pos_freq[word] += 1
            if entry['sentiment'].output == 'NEG':
                neg_freq[word] += 1
        if entry['lang'][0]['label'] not in counts:
            counts.add(entry['lang'][0]['label'])

    stop_words = []
    for lang in list(counts):
        stop_words += safe_get_stop_words(lang)
    stop_words = set(stop_words)

    for item in stop_words:
        if item in freq:
            del freq[item]
            if item in pos_freq.keys():
                del pos_freq[item]
            if item in neg_freq.keys():
                del neg_freq[item]
    if make_plot:
        wordcloud = WordCloud(width=2000,
                              height=1500,
                              random_state=1,
                              background_color='black',
                              relative_scaling=1,
                              margin=20,
                              colormap='Pastel1',
                              collocations=False,
                              stopwords=stop_words).generate_from_frequencies(freq)
        wordcloud.to_file(f'Word_cloud_all_{video_name}.png')
        wordcloud_pos = WordCloud(width=2000,
                                  height=1500,
                                  random_state=1,
                                  background_color='black',
                                  relative_scaling=1,
                                  margin=20,
                                  colormap='Pastel1',
                                  collocations=False,
                                  stopwords=stop_words).generate_from_frequencies(pos_freq)
        wordcloud_pos.to_file(f'Word_cloud_pos_{video_name}.png')
        wordcloud_neg = WordCloud(width=2000,
                                  height=1500,
                                  random_state=1,
                                  background_color='black',
                                  relative_scaling=1,
                                  margin=20,
                                  colormap='Pastel1',
                                  collocations=False,
                                  stopwords=stop_words).generate_from_frequencies(neg_freq)
        wordcloud_neg.to_file(f'Word_cloud_neg_{video_name}.png')

    return {'all_freq': freq, 'pos_freq': pos_freq, 'neg_freq': neg_freq}


def create_popularity_metrics(comments: dict,video_info:dict, video_name: str, analyser: Analyser = None, print_metrics=False):
    datetimes, cumulative_counts = plot_counts_by_datetime(comments, video_name)
    analyser = Analyser()
    metric_emotion = plot_counts_emotion(comments, video_name, analyser=analyser)
    # metric_likes_vs_replies = plot_like_vs_replies_counts(comments, video_name)
    metric_neq_pos = plot_counts_neg_and_pos(comments, video_name, analyser=analyser)
    favorite_count = int(video_info.get('favoriteCount', 0))
    comments_count = int(video_info.get('commentCount'), 0)
    likes_count = int(video_info.get('likeCount', 0))
    puplished_at = datetime.fromisoformat(video_info.get('publishedAt').replace('Z', '+00:00'))
    view_count = int(video_info.get('viewCount', 0))
    comments_size = len(cumulative_counts)
    comments_time_comp = 1
    if comments_size > 0:
        deltas = [(datetimes[i + 1] - datetimes[i]).seconds / 3600.0 for i in range(len(datetimes) - 1)]
        # calculate the first derivative of the count over time
        derivatives = [1.0 / deltas[i] for i in
                       range(len(cumulative_counts) - 1)]
        counts_coeff = np.log2(derivatives) if comments_size == 1 else 1
        comments_time_comp = np.mean(derivatives[:-counts_coeff])
        if comments_time_comp < 1:
            comments_time_comp = 1
    spam = 1+np.abs(comments_count - comments_size)/(max(comments_count, comments_size))
    time_delta = (datetime.now(timezone.utc) - puplished_at).total_seconds() / 60.0
    time_coeff = (likes_count + view_count*0.01)/time_delta
    comment_coeff = comments_size * spam * comments_time_comp
    em_coeff = (metric_neq_pos['Positive Comments'] + metric_neq_pos['Negative Comments'])/comments_size
    popularity = time_coeff + \
                 + favorite_count*25 + comment_coeff * em_coeff
    emotional_response = (metric_emotion['surprise'] + metric_emotion['joy']) - \
                         (metric_emotion['sadness'] + metric_emotion['anger'] + \
                          metric_emotion['fear']+metric_emotion['disgust'])
    if print_metrics:
        print('comments:', comments_size)
        print("spam:", spam)
        print("time_delta", time_delta)
        print("emotions",metric_emotion)
        print("p_n:", metric_neq_pos)
        print("likes", likes_count)
        print("views", view_count)
        print("time_coeff", time_coeff)
        print("deriv",comments_time_comp, derivatives[-counts_coeff])
        print("commets_coef", comment_coeff)
        print("em_coeff", em_coeff)
        print("poularity", popularity)
        print("response", emotional_response)


    return {'popularity':popularity, 'emotional_response':emotional_response}
