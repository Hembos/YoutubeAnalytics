import json
import googleapiclient.discovery


class Youtube():
    def __init__(self, youtube_api_key) -> None:
        self.videos: dict = None
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=youtube_api_key)

    def search_channels(self, category: str) -> list:
        request = self.youtube.search().list(
            part="snippet",
            maxResults=50,
            order="videoCount",
            q=category,
            type="channel"
        )

        response = request.execute()

        channels = list()

        for channel in response["items"]:
            channels.append(channel["id"]["channelId"])

        return channels

    def get_channel(self, channel_id: str) -> dict:
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics,brandingSettings",
            id=channel_id
        )
        response = request.execute()

        response_channel = response["items"][0]

        channel = {
            "title": response_channel["snippet"]["title"] if "title" in response_channel["snippet"] else None,
            "description": response_channel["snippet"]["description"] if "description" in response_channel["snippet"] else None,
            "customUrl": response_channel["snippet"]["customUrl"] if "customUrl" in response_channel["snippet"] else None,
            "publishedAt": response_channel["snippet"]["publishedAt"] if "publishedAt" in response_channel["snippet"] else None,
            "country": response_channel["snippet"]["country"] if "country" in response_channel["snippet"] else None,
            "viewCount": response_channel["statistics"]["viewCount"] if "viewCount" in response_channel["statistics"] else None,
            "subscriberCount": response_channel["statistics"]["subscriberCount"] if "subscriberCount" in response_channel["statistics"] else None,
            "hiddenSubscriberCount": response_channel["statistics"]["hiddenSubscriberCount"] if "hiddenSubscriberCount" in response_channel["statistics"] else None,
            "videoCount": response_channel["statistics"]["videoCount"] if "videoCount" in response_channel["statistics"] else None,
            "keywords": response_channel["brandingSettings"]["channel"]["keywords"] if "keywords" in response_channel["brandingSettings"]["channel"] else None
        }

        return channel

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

    def __del__(self) -> None:
        self.youtube.close()
