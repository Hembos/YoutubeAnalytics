from config.requests_types import *
from db.db import DataBase
from metrics.metric import *


def get_time_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    metric_data_time = plot_counts_by_datetime(comments, video_id)
    db.store_analisis(video_id, metric_data_time, GET_ANALYSIS_OF_TIME)


def get_lang_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    metric_count_langs = plot_counts_langs(comments, video_id, analyser=analyser)
    db.store_analisis(video_id, metric_count_langs, GET_ANALYSIS_OF_LANGUAGES)


def get_emotion_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    metric_emotion = plot_counts_emotion(comments, video_id, analyser=analyser)
    db.store_analisis(video_id, metric_emotion, GET_ANALYSIS_OF_EMOTION)


def get_likes_vs_replies_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    metric_likes_vs_replies = plot_like_vs_replies_counts(comments, video_id)
    db.store_analisis(video_id, metric_likes_vs_replies, GET_ANALYSIS_OF_LIKES_VS_REPLIES)


def get_neq_pos_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    metric_neq_pos = plot_counts_neg_and_pos(comments, video_id, analyser=analyser)
    db.store_analisis(video_id, metric_neq_pos, GET_ANALYSIS_OF_NEQ_POS)


def get_word_map(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    word_map = plot_word_map(comments, video_id, analyser=analyser)
    db.store_analisis(video_id, word_map, GET_WORD_MAP)


def get_popularity_analisis(data: dict, db: DataBase, analyser: Analyser) -> None:
    channel_id = data['channelId']
    video_id = data['videoId']
    comments = data['comments']
    video_info = data['video_info']
    popularity = create_popularity_metrics(comments,video_info, video_id, comments, analyser)
    db.store_analisis(video_id, popularity, GET_POPULARITY)

requests_func = {
    GET_ANALYSIS_OF_TIME: get_time_analisis,
    GET_ANALYSIS_OF_LANGUAGES: get_lang_analisis,
    GET_ANALYSIS_OF_EMOTION: get_emotion_analisis,
    GET_ANALYSIS_OF_LIKES_VS_REPLIES: get_likes_vs_replies_analisis,
    GET_ANALYSIS_OF_NEQ_POS: get_neq_pos_analisis,
    GET_POPULARITY: get_popularity_analisis,
    GET_WORD_MAP: get_word_map
}
