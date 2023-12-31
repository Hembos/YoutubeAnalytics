from config.quota_size import *
from core.youtube import Youtube
from queue import Queue
import logging
from db.db import DataBase
from core.requests_func import requests_func, requests_quota_size
from googleapiclient.errors import HttpError


def fetch(db: DataBase):
    youtube_api = None
    youtube = None

    while True:
        try:
            db.reset_api_quota()

            request = db.get_scraper_request(0, 6)
            print(request)

            if not request:
                continue

            request_quota_size = requests_quota_size[request["type"]]
            new_youtube_api = db.get_available_api(
                requests_quota_size[request["type"]])

            if not new_youtube_api:
                continue

            if youtube_api is None or youtube_api["key"] != new_youtube_api["key"]:
                youtube_api = new_youtube_api

                youtube = Youtube(youtube_api["key"])

            requests_func[request["type"]](youtube, request["data"], db)

            youtube_api["quota"] = youtube_api["quota"] - request_quota_size
            db.update_api_quota(youtube_api["key"], youtube_api["quota"])

            request["tasks_left"] -= 1
            db.update_scraper_request(request)
        except HttpError as e:
            print(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename="data.log", format="%(asctime)s %(levelname)s %(message)s")

    print("To exit the application, press Ctrl-c")

    db = DataBase()
    db.create_connection()

    try:
        fetch(db)
    except KeyboardInterrupt:
        logging.info("Ctrl-c was pressed")

    db.close_connection()
