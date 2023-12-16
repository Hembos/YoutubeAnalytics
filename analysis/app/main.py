import time

from db.db import DataBase
from emotion_analisis.analyser import Analyser
from metrics.loader import Loader

from requests_func import requests_func


def check_video(video_id, db: DataBase) -> bool:
    return db.is_video_exists(video_id)


def check_channel(channel_id: str, db: DataBase) -> bool:
    return db.is_channel_exists(channel_id)


def process(db: DataBase):
    analyser = Analyser()
    loader = Loader(db=db)
    while True:
        request = db.get_scraper_request(7, 13)
        if not request:
            continue
        video_id = request['data'].get('video_id')
        channel_id = request['data'].get('channel_id')
        if video_id and check_video(video_id, db):
            loader.load_video(video_id)
        if channel_id and check_channel(channel_id, db):
            loader.load_channel(channel_id)
        db.pre_update_request(request)
        data = {
            'channelId': channel_id,
            'videoId': video_id,
            'comments': loader.get_data_comments(channel_id, video_id),
            'video_info': loader.get_video_info(video_id, channel_id)
        }
        print(request)
        start_time = time.time()
        requests_func[request["type"]](data, db, analyser)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time: ', elapsed_time)
        request["tasks_left"] -= 1
        db.update_scraper_request(request)


if __name__ == "__main__":
    print("Analyser started")

    db = DataBase()
    db.create_connection()
    while True:
        try:
            process(db)
        except:
            continue
    db.close_connection()
