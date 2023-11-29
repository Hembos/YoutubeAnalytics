import logging

from collections import defaultdict
from analysis.app.db.db import DataBase
from analysis.app.metrics.loader import Loader

"""
Calculates metric -- number of comments depending on publication time
"""

import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter


def plot_counts_by_datetime(comments: dict, video_name: str) -> list:
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

    # Plot the graph
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


