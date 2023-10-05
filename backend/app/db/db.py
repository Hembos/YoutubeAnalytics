from config import mongodb_ip, mongodb_port, database_name, \
    ssh_connection, ssh_ip, ssh_password, ssh_username
from pymongo import MongoClient
from config.collections_names import *
from sshtunnel import SSHTunnelForwarder

import logging

from datetime import date


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

    def insert_video(self) -> bool:
        pass

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
