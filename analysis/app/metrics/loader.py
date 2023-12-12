
from collections.abc import Callable

from analysis.app.db.db import DataBase


class Loader:
    def __init__(self, channel_ids: list = None):
        self.channels = {}
        self.db = DataBase()
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
        self.db.create_connection()
        videos = self.db.get_videos(channel_id)
        for video in videos:
            videos[video]['comments'] = self.db.get_comments(video)
        self.db.close_connection()
        result = channel_id in self.channels.keys()
        self.channels[channel_id] = videos
        return result

    def get_all_comments(self, channel_id: str, video_id: str) -> dict:
        all_comments = {}
        for comment in self.channels[channel_id][video_id]['comments']:
            all_comments[comment['id']] = comment
        return all_comments



