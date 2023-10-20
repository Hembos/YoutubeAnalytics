from db.config import mongodb_ip, mongodb_port, database_name, \
    ssh_connection, ssh_ip, ssh_password, ssh_username
from pymongo import MongoClient
from db.config.collections_names import *
from sshtunnel import SSHTunnelForwarder

import logging

from datetime import date, datetime


class DataBase:
    def __init__(self) -> None:
        self.__server = None
        self.__db_connection = None
        self.__db = None

    def create_connection(self) -> bool:
        if ssh_connection:
            self.__server = SSHTunnelForwarder(ssh_ip, ssh_username=ssh_username,
                                               ssh_password=ssh_password, remote_bind_address=(mongodb_ip, mongodb_port))

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

    def get_available_api(self, min_quota_size) -> dict:
        query = {"quota": {"$gte": min_quota_size}}
        api = self.__db[API_KEYS].find_one(query)

        return api

    def update_api_quota(self, key, quota_size) -> bool:
        filter_query = {"key": key}
        update_query = {"$set": {"quota": quota_size}}

        return self.__db[API_KEYS].update_one(filter_query, update_query).raw_result["updatedExisting"]

    def reset_api_quota(self):
        today = date.today().isoformat()
        query_filter = {"last_reset": {"$lt": today}}
        update_query = {"$set": {"quota": 10000, "last_reset": today}}

        return self.__db[API_KEYS].update_many(query_filter, update_query).raw_result["updatedExisting"]

    def store_channel(self, channel: dict, channel_id: str, category: str) -> bool:
        filter_query = {"channel_id": channel_id}
        update_query = {"$set": channel}

        return self.__db[CHANNELS_COLLECTION_NAME].update_one(
            filter_query, update_query, upsert=True).raw_result["updatedExisting"]

    def store_video(self, video: dict, video_id: str) -> bool:
        filter_query = {"video_id": video_id}
        update_query = {"$set": video}

        return self.__db[VIDEOS_COLLECTION_NAME].update_one(
            filter_query, update_query, upsert=True).raw_result["updatedExisting"]

    def is_channel_exists(self, channel_id: str):
        query = {"channel_id": channel_id}
        return self.__db[CHANNELS_COLLECTION_NAME].find_one(query) != None

    def is_video_exists(self, video_id: str):
        query = {"video_id": video_id}
        return self.__db[VIDEOS_COLLECTION_NAME].find_one(query) != None

    def get_scraper_request(self):
        query = {"completed": False}
        request = self.__db[SCRAPER_REQUESTS].find_one(query)

        return request

    def update_scraper_request(self, request: dict):
        filter_query = {"_id": request["_id"]}

        if request["tasks_left"] <= 0:
            request["completed"] = True
            request["date_completion"] = datetime.today().isoformat()

        update_query = {"$set": request}
        return self.__db[SCRAPER_REQUESTS].update_one(filter_query, update_query, upsert=True).raw_result["updatedExisting"]

    def add_scraper_request(self, request: dict):
        return self.__db[SCRAPER_REQUESTS].insert_one(request)

    def store_comments(self, comments: dict, video_id: str) -> bool:
        query = {"video_id": video_id}

        comments_exists = self.__db[COMMENTS_COLLECTION_NAME].find_one(query)

        if comments_exists:
            comments["comments"] = comments_exists["comments"] + \
                comments["comments"]

        update_query = {"$set": comments}

        return self.__db[COMMENTS_COLLECTION_NAME].update_one(
            query, update_query, upsert=True).raw_result["updatedExisting"]
