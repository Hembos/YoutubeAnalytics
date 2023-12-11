from analysis.app.metrics.metric import *
from data.app.config.quota_size import *
from data.app.config.requests_types import *
from data.app.core.youtube import Youtube
from math import ceil

from data.app.db.db import DataBase


def get_channels_by_category(youtube: Youtube, data: dict, db: DataBase) -> None:
    channels_ids = youtube.search_channels(data["category"])

    for channel_id in channels_ids:
        request = {
            "type": GET_CHANNEL_BY_ID,
            "tasks_left": 1,
            "completed": False,
            "date_completion": None,
            "data": {
                "channel_id": channel_id,
                "category": data["category"]
            }
        }

        db.add_scraper_request(request)


def get_channel_by_id(youtube: Youtube, data: dict, db: DataBase) -> None:
    channel = youtube.get_channel(data["channel_id"])

    db.store_channel(channel, data["channel_id"], data["category"])

    playlist_id = data["channel_id"][:1] + 'U' + data["channel_id"][2:]

    request = {
        "type": GET_VIDEOS_BY_CHANNEL_ID,
        "tasks_left": ceil(float(channel["videoCount"]) / 50),
        "completed": False,
        "date_completion": None,
        "data": {
            "playlist_id": playlist_id,
            "pageToken": None
        }
    }

    db.add_scraper_request(request)


def get_channel_by_url(youtube: Youtube, data: dict, db: DataBase) -> None:
    channel = youtube.get_channel_by_url(data["channel_url"])

    db.store_channel(channel, channel["id"])

    playlist_id = channel["id"][:1] + 'U' + channel["id"][2:]

    request = {
        "type": GET_VIDEOS_BY_CHANNEL_ID,
        "tasks_left": ceil(float(channel["videoCount"]) / 50),
        "completed": False,
        "date_completion": None,
        "data": {
            "playlist_id": playlist_id,
            "pageToken": None
        }
    }

    db.add_scraper_request(request)


def get_channel_by_video_id(youtube: Youtube, data: dict, db: DataBase) -> None:
    channel = youtube.get_channel_by_video_id(data["video_id"])

    db.store_channel(channel, channel["id"])

    playlist_id = channel["id"][:1] + 'U' + channel["id"][2:]

    request = {
        "type": GET_VIDEOS_BY_CHANNEL_ID,
        "tasks_left": ceil(float(channel["videoCount"]) / 50),
        "completed": False,
        "date_completion": None,
        "data": {
            "playlist_id": playlist_id,
            "pageToken": None
        }
    }

    db.add_scraper_request(request)


def get_videos_by_channel_id(youtube: Youtube, data: dict, db: DataBase) -> None:
    next_page_token, videos_ids = youtube.get_videos(
        data["playlist_id"], data["pageToken"])

    for video_id in videos_ids:
        request = {
            "type": GET_VIDEO_BY_ID,
            "tasks_left": 1,
            "completed": False,
            "date_completion": None,
            "data": {
                "video_id": video_id,
            }
        }

        db.add_scraper_request(request)

    data["pageToken"] = next_page_token


def get_video_by_id(youtube: Youtube, data: dict, db: DataBase) -> None:
    video = youtube.get_video(data["video_id"])

    if video is None:
        return

    db.store_video(video, data["video_id"])

    if "commentCount" in video and video["commentCount"] != None:
        tasks_left = ceil(float(video["commentCount"]) / 100)
        if tasks_left > 0:
            request = {
                "type": GET_COMMENTS_BY_VIDEO_ID,
                "tasks_left": tasks_left,
                "completed": False,
                "date_completion": None,
                "data": {
                    "video_id": data["video_id"],
                    "pageToken": None
                }
            }

            db.add_scraper_request(request)


def get_comments_by_video_id(youtube: Youtube, data: dict, db: DataBase) -> None:
    next_page_token, comments = youtube.get_comments(
        data["video_id"], data["pageToken"])

    db.store_comments(comments)

    data["pageToken"] = next_page_token


def get_time_analisis(data: dict, db: DataBase) -> None:
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


def get_likes_vs_replies_analisis(data: dict, db: DataBase) -> None:
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


requests_func = {
    GET_CHANNELS_BY_CATEGORY: get_channels_by_category,
    GET_CHANNEL_BY_ID: get_channel_by_id,
    GET_VIDEOS_BY_CHANNEL_ID: get_videos_by_channel_id,
    GET_VIDEO_BY_ID: get_video_by_id,
    GET_COMMENTS_BY_VIDEO_ID: get_comments_by_video_id,
    GET_CHANNEL_BY_URL: get_channel_by_url,
    GET_CHANNEL_BY_VIDEO_ID: get_channel_by_video_id,
    GET_ANALYSIS_OF_TIME: get_time_analisis,
    GET_ANALYSIS_OF_LANGUAGES: get_lang_analisis,
    GET_ANALYSIS_OF_EMOTION: get_emotion_analisis,
    GET_ANALYSIS_OF_LIKES_VS_REPLIES: get_likes_vs_replies_analisis,
    GET_ANALYSIS_OF_NEQ_POS: get_neq_pos_analisis
}

requests_quota_size = {
    GET_CHANNELS_BY_CATEGORY: SEARCH_REQUEST,
    GET_CHANNEL_BY_ID: LIST_REQUEST,
    GET_VIDEOS_BY_CHANNEL_ID: LIST_REQUEST,
    GET_VIDEO_BY_ID: LIST_REQUEST,
    GET_COMMENTS_BY_VIDEO_ID: LIST_REQUEST,
    GET_CHANNEL_BY_URL: SEARCH_REQUEST + LIST_REQUEST,
    GET_CHANNEL_BY_VIDEO_ID: LIST_REQUEST + LIST_REQUEST
}
