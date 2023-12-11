from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Channel(BaseModel):
    channel_id: str
    country: str
    customUrl: str
    description: str
    hiddenSubscriberCount: int
    keywords: str
    publishedAt: datetime
    subscriberCount: int
    title: str
    videoCount: int
    viewCount: int

    class Config:
        allow_population_by_field_name = True


class ChannelsGroup(BaseModel):
    channels_id: List[str]


class ContentRating(BaseModel):
    pass


class Video(BaseModel):
    video_id: str
    caption: bool
    categoryId: str
    channelId: str
    commentCount: int
    contentRating: Optional[ContentRating]
    defaultAudioLanguage: str
    defaultLanguage: Optional[str]
    definition: str
    description: str
    dimension: str
    duration: str
    favoriteCount: int
    licensedContent: bool
    likeCount: int
    liveBroadcastContent: str
    projection: str
    publishedAt: str
    tags: List[str]
    title: str
    topicCategories: List[str]
    viewCount: int

    class Config:
        allow_population_by_field_name = True


class VideoGroup(BaseModel):
    videos_id: List[str]


class Comments(BaseModel):
    id: str
    authorChannelId: str
    authorChannelUrl: str
    authorDisplayName: str
    authorProfileImageUrl: str
    isReply: bool
    likeCount: int
    publishedAt: datetime
    textDisplay: str
    textOriginal: str
    totalReplyCount: int
    updatedAt: datetime
    videoId: str
    viewerRating: str

    class Config:
        allow_population_by_field_name = True


class ScrapData(BaseModel):
    channel_id: str = None
    channel_url: str = None
    category: str = None
    playlist_id: str = None
    pageToken: str = None
    video_id: str = None

    class Config:
        allow_population_by_field_name = True


class ScraperRequests(BaseModel):
    type: int
    tasks_left: int
    completed: bool
    date_completion: Optional[datetime]
    data: ScrapData

    class Config:
        allow_population_by_field_name = True


class User(BaseModel):
    login: str
    password: str
    video_groups_id: List[str]
    channel_groups_id: List[str]

    class Config:
        allow_population_by_field_name = True


class VideoMini(BaseModel):
    video_id: str
    title: str


class ChannelMini(BaseModel):
    channel_id: str
    title: str
    videos: List[VideoMini]
