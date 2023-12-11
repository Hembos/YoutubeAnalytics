import asyncio
from typing import List

from fastapi import APIRouter, Body, HTTPException

from app.models import ChannelMini
from app.db import collection_channels, collection_videos

router = APIRouter()

@router.get("/channels/", response_model=List[ChannelMini])
async def get_channels():
    channels = await collection_channels.find().to_list(length=None)
    if not channels:
        raise HTTPException(status_code=404, detail="No channels found")

    async def fetch_videos(channel_id):
        videos = await collection_videos.find({"channelId": channel_id}).to_list(length=None)
        return videos

    async def populate_videos(channel):
        channel_id = channel["channel_id"]
        videos = await fetch_videos(channel_id)
        channel["videos"] = videos
        return channel

    channels_with_videos = await asyncio.gather(*[populate_videos(channel) for channel in channels])
    return channels_with_videos
