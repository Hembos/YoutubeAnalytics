import unittest

from analysis.app.metrics.loader import Loader
from analysis.app.metrics.metric import plot_counts_by_datetime


class TestTimePlot(unittest.TestCase):
    def test_plot(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_counts_by_datetime(comments, test_video_id)


if __name__ == '__main__':
    unittest.main()
