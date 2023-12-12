import re
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import ScrapAnalyseRequests, RequestData
from app.db import requests_collection
from app.utils import remove_empty_values


def get_youtube_video_id(url):
    video_id = None

    pattern = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"

    match = re.search(pattern, url)
    if match:
        video_id = match.group(7)
    return video_id


router = APIRouter()


@router.post("/channel-by-category/", response_model=ScrapAnalyseRequests)
async def request_channel_downloading_by_category(category: str):
    scrap_data = RequestData(category=category)
    scraper_request = ScrapAnalyseRequests(type=0, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion', 'channel_id'])

    result = await requests_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-id/", response_model=ScrapAnalyseRequests)
async def request_channel_downloading_by_id(channel_id: str):
    scrap_data = RequestData(channel_id=channel_id)
    scraper_request = ScrapAnalyseRequests(type=1, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()
    request_dict = remove_empty_values(request_dict, ['date_completion', 'category'])
    result = await requests_collection.insert_one(request_dict)

    return request_dict


@router.post("/video-by-id/", response_model=ScrapAnalyseRequests)
async def request_channel_downloading_by_video_id(video_id: str):
    scrap_data = RequestData(video_id=video_id)
    scraper_request = ScrapAnalyseRequests(type=3, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await requests_collection.insert_one(request_dict)
    return request_dict


@router.post("/comments-by-video-id/", response_model=ScrapAnalyseRequests)
async def request_comments_downloading_by_video_id(video_id: str):
    scrap_data = RequestData(video_id=video_id)
    scraper_request = ScrapAnalyseRequests(type=4, tasks_left=None, completed=False, date_completion=None,
                                           data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['tasks_left', 'date_completion', 'pageToken'])

    result = await requests_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-url/", response_model=ScrapAnalyseRequests)
async def request_channel_downloading_by_url(channel_url: str):
    scrap_data = RequestData(channel_url=channel_url)
    scraper_request = ScrapAnalyseRequests(type=5, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await requests_collection.insert_one(request_dict)
    return request_dict


@router.post("/channel-by-video-url/", response_model=ScrapAnalyseRequests)
async def request_channel_downloading_by_video_url(video_url: str):
    video_id = None

    video_id = get_youtube_video_id(video_url)
    if video_id is None:
        raise HTTPException(status_code=400, detail="Invalid url")

    scrap_data = RequestData(video_id=video_id)
    scraper_request = ScrapAnalyseRequests(type=6, tasks_left=1, completed=False, date_completion=None, data=scrap_data)
    request_dict = scraper_request.model_dump()

    request_dict = remove_empty_values(request_dict, ['date_completion'])

    result = await requests_collection.insert_one(request_dict)
    return request_dict


@router.get("/requests/")
async def get_requests(count: int):
    requests = await requests_collection.find({}, {"_id": 0}).sort("_id", -1).limit(count).to_list(None)
    for request in requests:
        print(request)
    return requests
