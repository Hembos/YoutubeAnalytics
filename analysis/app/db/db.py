from config import mongodb_ip, mongodb_port, database_name, \
    ssh_connection, ssh_ip, ssh_password, ssh_username
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import logging

from datetime import date

from analysis.app.config.collections_names import CHANNELS_COLLECTION_NAME, COMMENTS_COLLECTION_NAME, \
    VIDEOS_COLLECTION_NAME


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

    def get_comments(self, video_id) -> list:
        comments = []
        for comment in self.__db[COMMENTS_COLLECTION_NAME].find({"videoId": video_id}):
            comments.append(comment)
        return comments

    def get_videos(self, channel_id) -> list:
        videos = []
        for video in self.__db[VIDEOS_COLLECTION_NAME].find({"channelId": channel_id}):
            videos.append(video)
        return  videos
