import datetime

from pymongo import MongoClient, UpdateOne
from sshtunnel import SSHTunnelForwarder

import logging

from datetime import date, datetime
from time import time

from app.db.config import *
from app.db.config.collections_names import *

from app.db.config.collections_names import *


class DataBase:
    def __init__(self) -> None:
        self.__server = None
        self.__db_connection = None
        self.__db = None

    def create_connection(self) -> bool:
        if ssh_connection:
            self.__server = SSHTunnelForwarder(ssh_ip, ssh_username=ssh_username,
                                               ssh_password=ssh_password,
                                               remote_bind_address=(mongodb_ip, mongodb_port))

            self.__server.start()

        self.__db_connection = MongoClient(
            mongodb_ip, self.__server.local_bind_port)
        self.__db = self.__db_connection[database_name]

    def close_connection(self) -> None:
        if self.__server:
            self.__server.stop()

        if self.__db_connection:
            self.__db_connection.close()

        logging.info("Close connection")

    def get_comments(self, video_id) -> list:
        return list(self.__db[COMMENTS_COLLECTION_NAME].find({"videoId": video_id}))

    def get_videos(self, channel_id) -> dict:
        videos = {}
        for video in self.__db[VIDEOS_COLLECTION_NAME].find({"channelId": channel_id}):
            videos[video['video_id']] = video
        return videos

    def get_video(self, video_id:str) -> dict:
        return dict(self.__db[VIDEOS_COLLECTION_NAME].find_one({"video_id": video_id}))

    def update_scraper_request(self, request: dict):
        filter_query = {"_id": request["_id"]}

        if request["tasks_left"] <= 0:
            request["completed"] = True
            request["date_completion"] = datetime.today().isoformat()

        update_query = {"$set": request}
        return self.__db[SCRAPER_REQUESTS].update_one(filter_query, update_query, upsert=True).raw_result[
            "updatedExisting"]

    def pre_update_request(self, request: dict):
        filter_query = {"_id": request["_id"]}

        request["completed"] = True

        update_query = {"$set": request}
        return self.__db[SCRAPER_REQUESTS].update_one(filter_query, update_query, upsert=True).raw_result[
            "updatedExisting"]
    def get_scraper_request(self, low_bound, upper_bound):

        return self.__db[SCRAPER_REQUESTS].find_one(
            {'type': {'$gte': low_bound, '$lte': upper_bound}, 'completed': False})

    def store_analisis(self, element_id, metric, param):
        data = {
            'id': element_id,
            'metric': metric,
            'type': param,
            'updated': datetime.today().isoformat()
        }
        filter_query = {"id": element_id, "type": param}
        update_query = {"$set": data}
        return self.__db[ANALYSIS_COLLECTION_NAME].update_one(filter_query, update_query, upsert=True).raw_result[
            "updatedExisting"]

    def is_channel_exists(self, channel_id: str):
        query = {"channel_id": channel_id}
        return self.__db[CHANNELS_COLLECTION_NAME].find_one(query) is not None

    def is_video_exists(self, video_id: str):
        query = {"video_id": video_id}
        return self.__db[VIDEOS_COLLECTION_NAME].find_one(query) is not None

    def get_all_metrics(self, metric_type):
        list(self.__db[ANALYSIS_COLLECTION_NAME].find({"type": metric_type }))

    def get_metric(self, video_id, metric_type):
        # todo fix
        if self.is_video_exists(video_id):
            d = dict(self.__db[ANALYSIS_COLLECTION_NAME].find_one({"type": metric_type, "id": video_id}))
            d = d.get('metric',{})
        else:
            d = [[],[]]
        if isinstance(d, list):
            d = {"0":d[0],"1":d[1]}
        return d