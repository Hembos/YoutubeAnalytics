from config.requests_types import *
from core.youtube import Youtube
from queue import Queue
from db.db import DataBase
from config.quota_size import *


def get_channels_by_category(youtube: Youtube, header: dict, requests_queue: Queue, db: DataBase) -> None:
    channels_ids = youtube.search_channels(header["category"])

    for channel_id in channels_ids:
        requests_queue.put(
            Request(LIST_REQUEST, GET_CHANNEL_BY_ID, {"channel_id": channel_id}))


def get_channel_by_id(youtube: Youtube, header: dict, requests_queue: Queue, db: DataBase) -> None:
    channel = youtube.get_channel(header["channel_id"])

    db.store_channel(channel, header["channel_id"])


def get_videos_by_channel_id(youtube: Youtube, header: dict, requests_queue: Queue, db: DataBase) -> None:
    pass


requests_func = {
    GET_CHANNELS_BY_CATEGORY: get_channels_by_category,
    GET_CHANNEL_BY_ID: get_channel_by_id,
    GET_VIDEOS_BY_CHANNEL_ID: get_videos_by_channel_id
}
