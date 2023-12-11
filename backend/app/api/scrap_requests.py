import re

from fastapi import APIRouter
from pydantic import BaseModel

from app.models import ScraperRequests, ScrapData
from app.db import scraper_collection


def get_youtube_video_id(url):
    video_id = None

    pattern = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"

    match = re.search(pattern, url)
    if match:
        video_id = match.group(7)
    return video_id


router = APIRouter()


def remove_empty_values(data, keep_keys):
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            cleaned_value = remove_empty_values(value, keep_keys)
            if cleaned_value:
                cleaned_data[key] = cleaned_value
        elif value is not None and value != "" or key in keep_keys:
            cleaned_data[key] = value
    return cleaned_data


@router.post("/channel-by-category/", response_model=ScraperRequests)
async def request_channel_downloading_by_category(category: str):
    scrap_data = ScrapData(category=category)
    scraper_request = ScraperRequests(type=0, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion', 'channel_id'])

    result = await scraper_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-id/", response_model=ScraperRequests)
async def request_channel_downloading_by_id(channel_id: str):
    scrap_data = ScrapData(channel_id=channel_id)
    scraper_request = ScraperRequests(type=1, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()
    request_dict = remove_empty_values(request_dict, ['date_completion', 'category'])
    result = await scraper_collection.insert_one(request_dict)

    return request_dict


@router.post("/video-by-id/", response_model=ScraperRequests)
async def request_channel_downloading_by_video_id(video_id: str):
    scrap_data = ScrapData(video_id=video_id)
    scraper_request = ScraperRequests(type=3, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await scraper_collection.insert_one(request_dict)
    return request_dict


@router.post("/comments-by-video-id/", response_model=ScraperRequests)
async def request_comments_downloading_by_video_id(video_id: str):
    scrap_data = ScrapData(video_id=video_id)
    scraper_request = ScraperRequests(type=4, tasks_left=None, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['tasks_left', 'date_completion', 'pageToken'])

    result = await scraper_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-url/", response_model=ScraperRequests)
async def request_channel_downloading_by_url(channel_url: str):
    scrap_data = ScrapData(channel_url=channel_url)
    scraper_request = ScraperRequests(type=5, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await scraper_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-video-url/", response_model=ScraperRequests)
async def request_channel_downloading_by_video_url(video_url: str):
    video_id = None

    video_id = get_youtube_video_id(video_url)

    scrap_data = ScrapData(video_id=video_id)
    scraper_request = ScraperRequests(type=6, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await scraper_collection.insert_one(request_dict)
    return request_dict
