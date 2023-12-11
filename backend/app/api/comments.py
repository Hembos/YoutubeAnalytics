from fastapi import APIRouter
from app.models import Comments
from typing import List

router = APIRouter()


@router.get("/comments/{comment_id}/", response_model=Comments)
def get_comment(comment_id: str):
    return comment_id


@router.get("/comments/", response_model=List[Comments])
async def get_comments_from_video(video_id: str):
    return video_id
