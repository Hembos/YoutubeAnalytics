from app.emotion_analisis.analyser import Analyser
from app.metrics.loader import Loader
from app.metrics.metric import plot_counts_by_datetime, plot_counts_neg_and_pos, plot_counts_emotion, \
    plot_like_vs_replies_counts, plot_counts_langs
test_video_id = 'q_ve9SsuyvU'
test_channel_id = 'UCzdmz_lLWT_dPqOvFjXAMVg'
loader = Loader([test_channel_id])
comments = loader.get_all_comments(test_channel_id, test_video_id)
plot_counts_langs(comments, test_video_id, make_plot=True)
