from config import mongodb_url, database_name
import pymongo
from config.collections_names import *


db_client = pymongo.MongoClient(mongodb_url)
db = db_client[database_name]

comments_collection = db[COMMENTS_COLLECTION_NAME]


def insert_video_comments(video_comments):

    comments_collection.insert_one(video_comments)
