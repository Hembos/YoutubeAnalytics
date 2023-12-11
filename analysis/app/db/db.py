from db.config import mongodb_ip, mongodb_port, database_name, \
    ssh_connection, ssh_ip, ssh_password, ssh_username
from pymongo import MongoClient, UpdateOne
from db.config.collections_names import *
from sshtunnel import SSHTunnelForwarder

import logging

from datetime import date, datetime
from time import time


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

    def get_comments(self, video_id, projection={"textDisplay": 1}) -> list:
        return list(self.__db[COMMENTS_COLLECTION_NAME].find({"videoId": video_id}, projection=projection))

    def get_videos(self, channel_id) -> dict:
        videos = {}
        for video in self.__db[VIDEOS_COLLECTION_NAME].find({"channelId": channel_id}):
            videos[video['video_id']] = video
        return videos
    
    def update_scraper_request(self, request: dict):
        filter_query = {"_id": request["_id"]}

        if request["tasks_left"] <= 0:
            request["completed"] = True
            request["date_completion"] = datetime.today().isoformat()

        update_query = {"$set": request}
        return self.__db[SCRAPER_REQUESTS].update_one(filter_query, update_query, upsert=True).raw_result["updatedExisting"]
