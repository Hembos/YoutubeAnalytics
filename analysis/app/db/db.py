
import datetime

from pymongo import MongoClient, UpdateOne
from db.config.collections_names import *
from sshtunnel import SSHTunnelForwarder

import logging

from datetime import date, datetime
from time import time

from analysis.app.db.config.collections_names import COMMENTS_COLLECTION_NAME, VIDEOS_COLLECTION_NAME, \
    ANALYSIS_COLLECTION_NAME
from data.app.db.config import ssh_ip, ssh_username, ssh_password, mongodb_ip, database_name


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

    def save_analysis(self, id, analysis) -> bool:
          data = {
              'id': id,
              'data': analysis,
              'time': datetime.datetime.utcnow()
          }
          self.__db[ANALYSIS_COLLECTION_NAME].update_one(data)