import time

from analysis.app.db.db import DataBase
from analysis.app.emotion_analisis.analyser import Analyser
from analysis.app.metrics.loader import Loader

from requests_func import requests_func


def check_video(video_id, db: DataBase) -> bool:
    return db.is_video_exists(video_id)


def check_channel(channel_id:str, db: DataBase) -> bool:
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
        data = {
            'channelId': channel_id,
            'videoId': video_id,
            'comments': loader.get_data_comments(channel_id, video_id)
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
    print("To exit the application, press Ctrl-c")

    db = DataBase()
    db.create_connection()

    process(db)

    db.close_connection()
