from typing import List

from fastapi import APIRouter, Body
from app.models import User
router = APIRouter()

@router.get("/user/{login}/", response_model=User)
def get_user(login: str):
    return login

@router.post("/user/", response_model=User)
async def create_user(user_create: User):
    return user_create