import logging
from collections import defaultdict

from analysis.app.emotion_analisis.analyser import Analyser

"""
Calculates metric -- number of comments depending on publication time
"""

import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter


def plot_counts_by_datetime(comments: dict, video_name: str, make_plot: bool = False) -> list:
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
    return [datetimes, cumulative_counts]


def plot_counts_neg_and_pos(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None:
        analyser.analyse_comments(comments)
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
    sizes = [positive_comments_count, negative_comments_count, neutral_comments_count]
    if make_plot:
        labels = ['Positive Comments', 'Negative Comments', 'Neutral Comments']
        colors = ['#66ff66', '#ff6666', '#999999']  # Green for positive, red for negative, gray for neutral
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_neg_and_pos_count_of_{video_name}.png')
    return sizes


def plot_counts_emotion(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None:
        analyser.analyse_comments(comments)
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
        plt.savefig(f'Comments_neg_and_pos_count_of_{video_name}.png')
    return sizes


def plot_like_vs_replies_counts(comments: dict, video_name: str, make_plot: bool = False):
    reply_count_dict = defaultdict(int)
    like_count_dict = defaultdict(int)
    for comment_id, comment_info in comments.items():
        is_reply = comment_info.get('isReply', False)
        like_count = comment_info.get('likeCount', 0)
        parent_id = comment_info.get('parentId', None)
        if is_reply:
            reply_count_dict[parent_id] += 1
            like_count_dict[parent_id] = like_count
        reply_counts = list(reply_count_dict.values())
        like_counts = list(like_count_dict.values())
        if make_plot:
            plt.scatter(reply_counts, like_counts, color='blue', alpha=0.5)
            plt.title(f'Like Count vs Reply Count {video_name}')
            plt.xlabel('Reply Count')
            plt.ylabel('Like Count')
            plt.savefig(f'Comments_likes_by_replies{video_name}.png')
    return reply_count_dict, like_count_dict


def plot_counts_langs(comments: dict, video_name: str, make_plot: bool = False, analyser: Analyser = None):
    if analyser is None:
        analyser = Analyser()
    if analyser.result is None:
        analyser.analyse_comments(comments)
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

def create_all_metrics(comments: dict, video_name: str, make_plot=False):
        metric_data_time = plot_counts_by_datetime(comments, video_name, make_plot)
        analyser = Analyser()
        metric_count_langs = plot_counts_langs(comments, video_name,make_plot, analyser=analyser)
        metric_emotion = plot_counts_emotion(comments, video_name,make_plot, analyser)
        metric_likes_vs_replies = plot_like_vs_replies_counts(comments, video_name,make_plot)
        metric_neq_pos = plot_counts_neg_and_pos(comments, video_name,make_plot, analyser)
        return {'metric_data_time':metric_data_time,
                'metric_count_langs':metric_count_langs,
                'metric_emotion':metric_emotion,
                'metric_likes_vs_replies':metric_likes_vs_replies,
                'metric_neq_pos':metric_neq_pos}
