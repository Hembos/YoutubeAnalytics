
from collections.abc import Callable

from analysis.app.db.db import DataBase


class Loader:
    def __init__(self, channel_ids: list = None, db: DataBase = None):
        self.channels = {}
        self.videos = {}
        self._is_test = False
        if db is None:
            self.db = DataBase()
            self._is_test = True
        else:
            self.db = db
        if channel_ids is not None:
            for channel_id in channel_ids:
                self.load_channel(channel_id)

    '''
    Load (or reload) channel info from db 
    
    Args:
        channel_id: id of a channel
    Returns:
        True if channel already existed    
    '''
    def load_channel(self, channel_id) -> bool:
        if self._is_test:
            self.db.create_connection()
        if channel_id in self.channels.keys():
            return True
        videos = self.db.get_videos(channel_id)
        for video in videos:
            if video in self.videos:
                videos[video]['comments'] = self.videos.pop(video)
                continue
            videos[video]['comments'] = self.db.get_comments(video)
        if self._is_test:
            self.db.close_connection()
        self.channels[channel_id] = videos
        return False

    def get_all_comments(self, channel_id: str, video_id: str) -> dict:
        all_comments = {}
        for comment in self.channels[channel_id][video_id]['comments']:
            all_comments[comment['id']] = comment
        return all_comments

    def load_video(self, video_id: str):
        if self._is_test:
            self.db.create_connection()
        if video_id in self.videos:
            return True
        self.videos[video_id] = dict()
        self.videos[video_id]['comments'] = self.db.get_comments(video_id)
        if self._is_test:
            self.db.close_connection()
        return False

    def get_data_comments(self, channel_id, video_id):
        comments = []
        if channel_id in self.channels:
            comments = self.channels[channel_id]['comments']
        if video_id in self.videos:
            comments = self.videos[video_id]['comments']
        all_comments = {}
        for comment in comments:
            all_comments[comment['id']] = comment
        return all_comments




