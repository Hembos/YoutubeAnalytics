from fastapi import APIRouter
from app.models import ScrapAnalyseRequests, RequestData
from app.utils import remove_empty_values
from app.db import requests_collection, collection_analysis

router = APIRouter()


@router.post("/build-video-analytics/{video_id}")
async def build_analytics_by_video_id(video_id: str):
    request = []
    for i in range(7, 14):
        req = ScrapAnalyseRequests(type=i, tasks_left=1, completed=False, date_completion=None,
                                   data=RequestData(video_id=video_id))
        req = remove_empty_values(req.model_dump(), ['date_completion'])
        request.append(req)
    result = await requests_collection.insert_many(request)
    for i in request:
        i.pop('_id')
    return request


@router.post("/build-channel-analytics/{channel_id}")
async def build_analytics_by_channel_id(channel_id: str):
    request = []
    for i in range(7, 14):
        req = ScrapAnalyseRequests(type=i, tasks_left=1, completed=False, date_completion=None,
                                   data=RequestData(channel_id=channel_id))
        req = remove_empty_values(req.model_dump(), ['date_completion'])
        request.append(req)
    result = await requests_collection.insert_many(request)
    for i in request:
        i.pop('_id')
    return request


@router.get("/get-analytics/{type}/{id}")
async def get_analytics_by_type_and_id(type: int, id: str):
    result = await collection_analysis.find({"type": type, "id": id}).to_list(length=None)
    if len(result) == 1:
        result = result[0]
        result.pop("_id")
    elif len(result) == 0:
        result = {"result": "not found"}
    else:
        result = {"result": "too many matching objects"}
    return result
