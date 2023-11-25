from config.requests_types import *
from core.youtube import Youtube
from queue import Queue
from db.db import DataBase
from config.quota_size import *
from math import ceil


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
        "tasks_left": ceil(float(channel["videoCount"])/50),
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
        "tasks_left": ceil(float(channel["videoCount"])/50),
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
        tasks_left = ceil(float(video["commentCount"])/100)
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


requests_func = {
    GET_CHANNELS_BY_CATEGORY: get_channels_by_category,
    GET_CHANNEL_BY_ID: get_channel_by_id,
    GET_VIDEOS_BY_CHANNEL_ID: get_videos_by_channel_id,
    GET_VIDEO_BY_ID: get_video_by_id,
    GET_COMMENTS_BY_VIDEO_ID: get_comments_by_video_id,
    GET_CHANNEL_BY_URL: get_channel_by_url
}

requests_quota_size = {
    GET_CHANNELS_BY_CATEGORY: SEARCH_REQUEST,
    GET_CHANNEL_BY_ID: LIST_REQUEST,
    GET_VIDEOS_BY_CHANNEL_ID: LIST_REQUEST,
    GET_VIDEO_BY_ID: LIST_REQUEST,
    GET_COMMENTS_BY_VIDEO_ID: LIST_REQUEST,
    GET_CHANNEL_BY_URL: SEARCH_REQUEST + LIST_REQUEST,
}
