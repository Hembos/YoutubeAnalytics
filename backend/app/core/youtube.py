import json
# from decouple import config
import googleapiclient.discovery
from config import youtube_api_keys


class Youtube():
    def __init__(self) -> None:
        self.videos: dict = None
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=youtube_api_keys[0])

    def read_videos_from_file(self, file_name: str) -> None:
        with open(file_name, "r") as f:
            self.videos = json.load(f)

    def fetch_video(self, video_id: str):
        if self.videos is None:
            self.videos = {}

        if video_id not in self.videos:
            self.videos[video_id] = {}

        self.videos[video_id]["comments"] = self.__fetch_comments(video_id)

    def __fetch_comments(self, video_id: str) -> list:
        request = self.youtube.commentThreads().list(
            part="snippet, replies",
            maxResults=100,
            videoId=video_id,
            textFormat="plainText",
        )
        response = request.execute()

        comments = response["items"]

        while response:
            if 'nextPageToken' in response:
                response = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    maxResults=100,
                    videoId=video_id,
                    textFormat="plainText",
                    pageToken=response['nextPageToken']
                ).execute()

                comments = comments + response["items"]
            else:
                break

        return comments

    def save_videos_to_file(self, file_name: str) -> None:
        with open(file_name, "w") as f:
            f.write(json.dumps(self.videos, indent=4))
