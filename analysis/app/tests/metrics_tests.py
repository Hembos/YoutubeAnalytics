import unittest

from matplotlib import pyplot as plt

from analysis.app.emotion_analisis.analyser import Analyser
from analysis.app.metrics.loader import Loader
from analysis.app.metrics.metric import plot_counts_by_datetime, plot_counts_neg_and_pos, plot_counts_emotion, \
    plot_like_vs_replies_counts, plot_counts_langs, create_all_metrics


class TestAnalisis(unittest.TestCase):
    def test_sentiment(self):
        test_comment_text = 'Love this video'
        analyser = Analyser()
        res = analyser.analyse_sentiment(test_comment_text)

    def test_plot_time(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_counts_by_datetime(comments, test_video_id)

    def test_plot_pos_neg_count(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_counts_neg_and_pos(comments, test_video_id, make_plot=True)

    def test_plot_emotion(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_counts_emotion(comments, test_video_id, make_plot=True)

    def test_pie_plot(self):
        sizes = [20, 10, 70]
        labels = ['Positive Comments', 'Negative Comments', 'Neutral Comments']
        colors = ['#66ff66', '#ff6666', '#999999']  # Green for positive, red for negative, gray for neutral
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_neg_and_pos_count_of_test.png')

    def test_emotions_calc(self):
        types = ['others', 'joy', 'sadness', 'anger', 'surprise', 'disgust', 'fear']
        plt.pie([i for i in range(len(types))], labels=types, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.savefig(f'Comments_emotion_test.png')

    def test_plot_like_vs_replies_counts(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_like_vs_replies_counts(comments, test_video_id, make_plot=True)

    def test_plot_langs(self):
        test_video_id = 'q_ve9SsuyvU'
        test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
        loader = Loader([test_channel_id])
        comments = loader.get_all_comments(test_channel_id, test_video_id)
        plot_counts_langs(comments, test_video_id, make_plot=True)

    def test_plot_ru_langs(self):
        comments = {
            'test1':{
            'id':'test',
            'textOriginal':"Мне нравится"}
        }
        plot_counts_langs(comments, 'test_name', make_plot=True)
    def test_all(self):
        v_id ='g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        comments = loader.get_all_comments(ch_id, v_id)
        mets = create_all_metrics(comments, v_id, True)

if __name__ == '__main__':
    unittest.main()